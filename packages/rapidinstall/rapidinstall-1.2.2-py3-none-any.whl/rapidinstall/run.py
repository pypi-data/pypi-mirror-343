# rapidinstall/src/rapidinstall/run.py

import subprocess
import time
import threading
import queue
import os
import sys
import logging
from typing import List, Dict, Any, Optional, Tuple, Set
import re
import weakref
import shutil
import signal
import json
import tempfile
from collections import defaultdict, deque


try:
    from rapidinstall import pip_concurrent
except ImportError:
    pip_concurrent = None

pySmartDL = None

# --- Configuration ---
DEFAULT_STATUS_UPDATE_INTERVAL = 30
SEPARATOR = "*" * 60
ANSI_ESCAPE_REGEX = re.compile(r"\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
TASK_STATUS_SENTINEL = "_task_status"
DRY_RUN_SLEEP_DURATION = 20

# --- Helper Function for Late Import ---


def _import_pysmartdl():
    global pySmartDL
    if pySmartDL is None:
        try:
            import pySmartDL as pysmartdl_module

            pySmartDL = pysmartdl_module
        except ImportError:
            raise ImportError(
                "The 'pySmartDL' package is required for download tasks. "
                "Please install it using: pip install rapidinstall[download]"
            )
    return pySmartDL


class RapidInstaller:

    """
    Manages parallel command and download tasks. Downloads can be moved
    to a final destination after all tasks complete using the 'move_to' parameter.
    """

    def __init__(
        self,
        update_interval: Optional[int] = DEFAULT_STATUS_UPDATE_INTERVAL,
        verbose: bool = True,
        exit_on_interrupt: bool = True,
        dryrun: bool = False, # Added dryrun parameter
    ):
        self._update_interval = (
            update_interval
            if update_interval is not None and update_interval > 0
            else 0
        )
        self._verbose = verbose
        self._exit_on_interrupt = exit_on_interrupt
        self._dryrun = dryrun # Store dryrun flag
        self._setup_signal_handlers()

        self._logger = logging.getLogger(f"RapidInstaller-{id(self)}")
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.propagate = False
        if verbose:
            self._logger.setLevel(logging.INFO)
        else:
            self._logger.setLevel(logging.WARNING)

        self._print_lock = threading.Lock()
        self._state_lock = threading.Lock()
        # _active_tasks structure potentially enhanced for dry run
        self._active_tasks: Dict[str, Dict[str, Any]] = {}
        self._final_results: Dict[str, Dict[str, Any]] = {}
        self._monitor_thread: Optional[threading.Thread] = None
        self._monitor_thread_started = threading.Event()
        self._stop_monitor_event = threading.Event()
        self._instance_active = True
        self._deferred_moves = []
        self._on_task_start = None
        self._on_task_complete = None

        # Pip related state
        self._pip_tasks: List[Tuple[Any, Dict]] = [] # Stores (packages, options)
        self._pip_resolution_done: bool = False
        self._pip_install_failed: bool = False

        if self._dryrun:
            self._print_locked("--- DRY RUN MODE ENABLED ---")
            self._print_locked(f"--- Tasks will be simulated with a {DRY_RUN_SLEEP_DURATION}s delay ---")

    def _setup_signal_handlers(self):
        """Set up signal handlers for graceful shutdown on keyboard interrupt."""

        def signal_handler(sig, frame):
            # Make the handler a no-op if we're already shutting down
            if not self._instance_active:
                return

            if sig == signal.SIGINT:
                # Print a message to indicate shutdown is in progress
                print("\n\nKeyboard interrupt received (Ctrl+C). Gracefully shutting down...",
                        file=sys.stderr)

                self._interrupt_received = True

        # Register the handler for SIGINT (Ctrl+C)
        signal.signal(signal.SIGINT, signal_handler)
        self._interrupt_received = False

    def _ensure_monitor_running(self):
        """
        Ensures the monitor thread is running to track task progress.
        Creates and starts a new monitor thread if needed.
        """
        if not self._instance_active:
            raise RuntimeError("Cannot add tasks after wait() or shutdown().")

        with self._state_lock:
            if self._monitor_thread is None or not self._monitor_thread.is_alive():
                #self._print_locked("Starting monitor thread...")
                self._stop_monitor_event.clear()
                self._monitor_thread_started.clear()
                self._monitor_thread = threading.Thread(
                    target=self._monitor_loop, daemon=True
                )
                self._monitor_thread.start()
                # Wait briefly for the monitor thread to signal it has started
                if not self._monitor_thread_started.wait(timeout=5):
                    self._print_locked(
                        "Warning: Monitor thread did not signal start within timeout.",
                        level=logging.WARNING
                    )

    def _print_status_block(self, header, lines=None, separator=SEPARATOR):
        """
        Print a consistently formatted status block.

        Args:
            header (str): The header text (will be prefixed with '* ')
            lines (list, optional): List of lines to print (each will be prefixed with '* ')
            separator (str): The separator string to use (default is SEPARATOR)
        """
        with self._print_lock:
            self._logger.info(f"\n{separator}")
            self._logger.info(f"* {header}")

            if lines:
                for line in lines:
                    if isinstance(line, str):
                        # Split multi-line content and prefix each line
                        for subline in line.splitlines():
                            if subline.strip():  # Skip empty lines
                                self._logger.info(f"* {subline}")

            self._logger.info(f"{separator}")

    def add_pip(self, packages, extra_index_urls=None, upgrade=False, pip_options=None):
        """
        Registers pip installation requests. Resolution and installation occur later
        during wait() or when pip_check_dependencies_and_install() is called.

        Args:
            packages: String or list of package specifications (pip-like syntax allowed in string).
            extra_index_urls: Optional list/string of extra index URLs.
            upgrade: If True, add --upgrade flag.
            pip_options: Dictionary of additional pip options (e.g., {"no-cache-dir": True}).
        """
        if self._pip_resolution_done:
                self._print_locked("Warning: Cannot add pip tasks after dependency resolution has run.", level=logging.WARNING)
                return

        pip_cmd_parts = []
        parsed_extra_urls = []
        parsed_index_url = None # Track primary index URL if specified

        # Consolidate pip_options dict to list of command parts
        # Example: {"no-cache-dir": True, "timeout": 60} -> ["--no-cache-dir", "--timeout=60"]
        if pip_options:
            for key, value in pip_options.items():
                opt_name = f"--{key.replace('_', '-')}"
                if isinstance(value, bool) and value:
                    pip_cmd_parts.append(opt_name)
                elif not isinstance(value, bool):
                    pip_cmd_parts.append(f"{opt_name}={value}")

        # Parse string input (pip-like format)
        if isinstance(packages, str):
            parts = packages.strip().split()
            pkg_list = []
            i = 0
            while i < len(parts):
                part = parts[i]
                if part in ['-i', '--index-url']:
                    if i + 1 < len(parts):
                        # Only store the last specified index-url
                        parsed_index_url = parts[i+1]
                        i += 2
                    else:
                        raise ValueError(f"Missing URL after {part}")
                elif part.startswith('-i='):
                    parsed_index_url = part[3:]
                    i += 1
                elif part.startswith('--index-url='):
                    parsed_index_url = part.split('=', 1)[1]
                    i += 1
                elif part == '--extra-index-url':
                    if i + 1 < len(parts):
                        parsed_extra_urls.append(parts[i+1])
                        i += 2
                    else:
                        raise ValueError(f"Missing URL after {part}")
                elif part.startswith('--extra-index-url='):
                    parsed_extra_urls.append(part.split('=', 1)[1])
                    i += 1
                elif part.startswith('-'):
                    # Other pip options directly in the string
                    pip_cmd_parts.append(part)
                    if part in ['-r', '--requirement'] and i + 1 < len(parts): # Handle flags with args
                            pip_cmd_parts.append(parts[i+1])
                            i += 1
                    i += 1
                else:
                    # Must be a package spec
                    pkg_list.append(part)
                    i += 1
            packages = pkg_list
        elif isinstance(packages, list):
            pass # Already a list
        else:
            raise TypeError("packages must be a string or list")

        # Handle extra_index_urls parameter
        if extra_index_urls:
            if isinstance(extra_index_urls, str):
                parsed_extra_urls.append(extra_index_urls)
            elif isinstance(extra_index_urls, list):
                parsed_extra_urls.extend(extra_index_urls)

        if not packages:
            self._print_locked("Warning: No packages specified in add_pip call.", level=logging.WARNING)
            return

        # Store the parsed info
        options = {
            "index_url": parsed_index_url, # Store separately
            "extra_index_urls": list(set(parsed_extra_urls)), # Deduplicate
            "upgrade": upgrade,
            "additional_args": list(set(pip_cmd_parts)), # Deduplicate basic flags
        }

        with self._state_lock:
            self._pip_tasks.append((packages, options))
        self._print_locked(f"Queued pip request for: {' '.join(packages)}")

    def add_tasks(self, tasks: List[Dict[str, Any]]):
        """
        Add multiple command tasks at once.
        """
        for task in tasks:
            self.add_task(**task)

    def on_task_start(self, callback):
        """
        Register a callback function to be called when a task starts.
        """
        self._on_task_start = callback

    def on_task_complete(self, callback):
        """
        Register a callback function to be called when a task completes.
        """
        self._on_task_complete = callback

    # --- Helper Methods ---
    def _print_locked(self, *args, level=logging.INFO, **kwargs):
        with self._print_lock:
            if level == logging.ERROR:
                self._logger.error(*args, **kwargs)
            elif level == logging.WARNING:
                self._logger.warning(*args, **kwargs)
            else:
                if self._verbose:
                    self._logger.info(*args, **kwargs)

    @staticmethod
    def _strip_ansi(text: str) -> str:
        return ANSI_ESCAPE_REGEX.sub("", text)

    @staticmethod
    def _format_output_block(title: str, content: str) -> str:
        if not content.strip():
            return ""
        return f"{SEPARATOR}\n{title}\n{SEPARATOR}\n{content.strip()}\n{SEPARATOR}\n"

    @staticmethod
    def _process_status_lines(lines: List[str]) -> str:
        processed_output, current_line = "", ""
        for raw_line in lines:
            stripped_line = RapidInstaller._strip_ansi(raw_line)
            parts = stripped_line.split("\r")
            if len(parts) > 1:
                current_line = parts[-1]
            else:
                current_line += parts[0]
            if raw_line.endswith("\n"):
                processed_output += current_line
                current_line = ""
        if current_line:
            processed_output += current_line
        if lines and lines[-1].endswith("\n") and not processed_output.endswith("\n"):
            processed_output += "\n"
        return processed_output.strip()

    @staticmethod
    def _stream_reader(
        stream,
        output_queue: queue.Queue,
        stream_name: str,
        process_ref: weakref.ReferenceType,
    ):
        # ... (unchanged)
        try:
            for line in iter(stream.readline, ""):
                if process_ref() is None:
                    break
                if line:
                    output_queue.put((stream_name, line))
                else:
                    break
        except ValueError:
            pass
        except Exception as e:
            # Attempt to report the error, but don't crash the reader thread if the queue fails
            error_line = (
                f"[{stream_name}] Error reading stream: {type(e).__name__}: {e}\n"
            )
            try:
                output_queue.put(("stderr", error_line))
            except Exception:
                pass  # Ignore queue errors during error reporting
        finally:
            # Signal that this reader is done (important for knowing when to join)
            try:
                output_queue.put((stream_name, None))  # Sentinel value
            except Exception:
                pass  # Ignore queue errors during final signal
            # Don't close the stream here, the Popen object owns it.

    # --- Download Execution Function (using pySmartDL) ---
    @staticmethod
    def _execute_download_pysmartdl(
        url: str,
        initial_dest_path: str,
        output_queue: queue.Queue,
        task_name: str,
        verbose: bool,
    ):
        """Performs the download using pySmartDL, reports basic status via queue."""
        try:
            _pysdl = _import_pysmartdl()
        except ImportError as e:
            try:
                output_queue.put(("stderr", f"[{task_name}:stderr] {e}\n"))
                output_queue.put((TASK_STATUS_SENTINEL, (1, None)))  # RC=1, final_path=None
            except Exception:
                pass
            return

        return_code = 1  # Default failure
        final_filepath = None  # Track the actual final path pySmartDL used

        def _put_q(stream, msg):
            try:
                output_queue.put((stream, f"[{task_name}:{stream}] {msg.strip()}\n"))
            except Exception:
                pass  # Ignore queue errors here

        try:
            target_dir = os.path.dirname(initial_dest_path)
            if target_dir:
                os.makedirs(target_dir, exist_ok=True)

            _put_q("stdout", f"Starting download from {url} (Task: {task_name})")

            # Use dest_param logic as before
            dest_param = (
                target_dir
                if os.path.basename(initial_dest_path) == ""
                else initial_dest_path
            )

            # Create downloader
            downloader = _pysdl.SmartDL(
                url, dest=dest_param, progress_bar=False, timeout=120
            )

            # Set up progress reporting with better persistence
            stop_progress = threading.Event()
            progress_lock = threading.Lock()
            last_progress_info = {"text": "Starting...", "timestamp": time.time()}

            # Define function to update progress info
            def update_progress_info(info_text):
                with progress_lock:
                    last_progress_info["text"] = info_text
                    last_progress_info["timestamp"] = time.time()
                    # Always send the latest progress to the queue
                    _put_q("stdout", f"PROGRESS:{info_text}")

            def report_progress():
                update_progress_info("Starting...")  # Initial status

                try:
                    # Start the actual download (non-blocking)
                    downloader.start(blocking=False)

                    # Monitor progress until explicitly stopped
                    while not stop_progress.is_set():
                        try:
                            # Check download status
                            if downloader.isFinished():
                                update_progress_info("Finalizing...")
                                break

                            # Get progress information
                            progress_pct = downloader.get_progress() * 100

                            # Sometimes get_speed() can fail during early stages
                            try:
                                dl_speed = downloader.get_speed(human=True)
                            except:
                                dl_speed = "? KB/s"

                            # Get downloaded bytes
                            try:
                                dl_size = downloader.get_dl_size(human=True)
                            except:
                                dl_size = "? MB"

                            # Try to get total size
                            try:
                                total_size = downloader.get_total_size(human=True)
                            except:
                                total_size = "Unknown"

                            # Format progress message
                            size_info = f"{dl_size}/{total_size}" if total_size != "Unknown" else dl_size
                            progress_msg = f"{progress_pct:.1f}%|{dl_speed}|{size_info}"

                            # Update the persistent progress info
                            update_progress_info(progress_msg)
                        except Exception as e:
                            # Log error but continue reporting
                            _put_q("stderr", f"Progress report error: {e}")

                        # Sleep for a short time before next update (don't use too long a delay)
                        time.sleep(0.5)

                    # Wait for download to complete if it's still going
                    if not downloader.isFinished():
                        update_progress_info("Waiting for download to complete...")
                        downloader.wait()

                    update_progress_info("Download complete")

                except Exception as e:
                    update_progress_info(f"Progress error: {e}")
                    # Don't re-raise - let the main thread handle errors

            # Start progress reporting in a thread
            progress_thread = threading.Thread(target=report_progress, daemon=True)
            progress_thread.start()

            # Wait for download to finish
            try:
                # Wait for progress thread instead of blocking download
                while progress_thread.is_alive() and not downloader.isFinished():
                    time.sleep(1)

                # Ensure download is fully complete
                if not downloader.isFinished():
                    downloader.wait()
            finally:
                # Stop progress thread
                stop_progress.set()
                progress_thread.join(timeout=2)

            # The rest of the function remains the same
            final_filepath = downloader.get_dest()

            if downloader.isSuccessful():
                duration = downloader.get_dl_time()
                final_size = downloader.get_final_filesize()
                size_mb = final_size / (1024 * 1024) if final_size else 0
                size_str = f"{size_mb:.2f} MB" if size_mb else f"{final_size} bytes"
                _put_q(
                    "stdout",
                    f"Download completed: '{os.path.basename(final_filepath)}' ({size_str} in {duration:.2f}s)",
                )
                return_code = 0
            else:
                errors = downloader.get_errors()
                error_str = ", ".join(map(str, errors)) if errors else "Unknown error"
                _put_q("stderr", f"Download failed: {error_str}")
                if final_filepath and os.path.exists(final_filepath):
                    try:
                        os.remove(final_filepath)
                        _put_q("stderr", "Removed partial file.")
                    except OSError:
                        pass  # Ignore cleanup errors

        except OSError as e:
            _put_q("stderr", f"Download failed: OS error preparing - {e}")
        except Exception as e:
            _put_q(
                "stderr", f"Download failed: Unexpected error - {type(e).__name__}: {e}"
            )
            # Use initial_dest_path for cleanup attempt if downloader object failed early
            cleanup_path = final_filepath or initial_dest_path
            if os.path.exists(cleanup_path):
                try:
                    os.remove(cleanup_path)
                    _put_q("stderr", f"Removed partial/target file: {cleanup_path}")
                except OSError as remove_err:
                    _put_q(
                        "stderr",
                        f"Error removing partial/target file {cleanup_path}: {remove_err}",
                    )
        finally:
            # Signal completion: (return_code, actual_final_path)
            try:
                output_queue.put((TASK_STATUS_SENTINEL, (return_code, final_filepath)))
            except Exception as q_err:
                # Non-critical, but log it. Failing to put status might cause issues.
                print(
                    f"[{task_name}:ERROR] Failed to put final status on queue: {q_err}",
                    file=sys.stderr,
                )

    # --- Public Task Management Methods ---

    def add_task(self, name: str, commands: str) -> Optional[Dict[str, Any]]:
        """
        Adds and starts a shell command task, or simulates it in dry run mode.

        Returns:
            A dictionary containing tracking information for the task (real or simulated),
            or None if the task could not be started.
        """
        if not name:
            raise ValueError("Task 'name' cannot be empty.")
        if not commands:
            raise ValueError("Task 'commands' cannot be empty.")

        self._ensure_monitor_running() # Ensure monitor runs even for dry run tasks
        task_info = None

        with self._state_lock:
            if name in self._active_tasks or name in self._final_results:
                self._print_locked(
                    f"Warning: Task '{name}' already exists. Skipping.", level=logging.WARNING
                )
                return None

            # Initialize result placeholder
            self._final_results[name] = {
                "type": "command",
                "stdout": "",
                "stderr": "Submitted...",
                "returncode": None,
                "pid": None,
                "start_time": None,
                "duration_sec": None,
                "dryrun": self._dryrun, # Indicate if it was a dry run
            }

            start_time = time.time()

            if self._dryrun:
                self._print_status_block(
                    f"[DRYRUN] Task '{name}' (command)",
                    [f"Command: {commands[:150]}{'...' if len(commands) > 150 else ''}",
                        f"Simulating {DRY_RUN_SLEEP_DURATION}s execution..."]
                )
                if self._on_task_start:
                        try: self._on_task_start(name, "command", dryrun=True)
                        except Exception: pass # Ignore callback errors

                # Create dummy task info for monitoring
                dry_run_completion_event = threading.Event()
                # Use a timer to signal completion after the sleep duration
                timer = threading.Timer(DRY_RUN_SLEEP_DURATION, dry_run_completion_event.set)
                timer.daemon = True
                timer.start()

                task_info = {
                    "type": "command",
                    "name": name,
                    "process": None, # No real process
                    "pid": None,
                    "output_queue": None, # No output queue
                    "stream_reader_threads": [],
                    "start_time": start_time,
                    "final_output": {"stdout": [f"[DRYRUN] Would execute: {commands}\n"], "stderr": []},
                    "task_status_code": 0, # Assume success for dry run
                    "final_filepath": None,
                    "dryrun": True,
                    "dryrun_completion_event": dry_run_completion_event, # Event to check
                    "dryrun_timer": timer, # Keep ref to timer
                }
                self._active_tasks[name] = task_info
                self._final_results[name].update({
                    "start_time": start_time,
                    "stderr": "",
                    "stdout": f"[DRYRUN] Would execute: {commands}\n",
                })

            else: # Real execution
                try:
                    output_q = queue.Queue()
                    env = os.environ.copy()
                    env["PYTHONUNBUFFERED"] = "1"

                    process = subprocess.Popen(
                        commands,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        bufsize=1, # Line buffered
                        env=env,
                        # On Windows, use creationflags to prevent new console window
                        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
                        start_new_session=True # Try to make it easier to terminate children later if needed
                    )
                    process_ref = weakref.ref(process)

                    stdout_reader = threading.Thread(
                        target=RapidInstaller._stream_reader,
                        args=(process.stdout, output_q, "stdout", process_ref),
                        daemon=True,
                    )
                    stderr_reader = threading.Thread(
                        target=RapidInstaller._stream_reader,
                        args=(process.stderr, output_q, "stderr", process_ref),
                        daemon=True,
                    )
                    stdout_reader.start()
                    stderr_reader.start()

                    self._print_status_block(
                        f"STARTED Task '{name}' (command)",
                        [f"PID: {process.pid}", f"Command: {commands[:100]}{'...' if len(commands) > 100 else ''}"]
                    )
                    if self._on_task_start:
                            try: self._on_task_start(name, "command", dryrun=False)
                            except Exception: pass

                    task_info = {
                        "type": "command",
                        "name": name,
                        "process": process, # The actual process object
                        "thread": None,
                        "pid": process.pid,
                        "output_queue": output_q,
                        "stream_reader_threads": [stdout_reader, stderr_reader],
                        "start_time": start_time,
                        "final_output": {"stdout": [], "stderr": []},
                        "task_status_code": None,
                        "final_filepath": None,
                        "dryrun": False,
                    }
                    self._active_tasks[name] = task_info
                    self._final_results[name].update(
                        {"start_time": start_time, "pid": process.pid, "stderr": ""}
                    )

                except Exception as e:
                    err_msg = f"ERROR starting command '{name}': {e}"
                    self._print_locked(f"  {err_msg}")
                    self._final_results[name].update(
                        {"stderr": err_msg, "returncode": -1, "start_time": start_time} # Use start_time even if failed
                    )
                    if name in self._active_tasks: del self._active_tasks[name]
                    return None # Indicate failure to start

        return task_info # Return tracking info

    def add_download(
            self,
            url: str,
            name: str,
            directory: Optional[str] = None,
            move_to: Optional[str] = None,
        ) -> Optional[Dict[str, Any]]: # Added return type hint
            """
            Adds and starts a download task, or simulates it in dry run mode.

            Returns:
                 A dictionary containing tracking information for the task (real or simulated),
                 or None if the task could not be started (e.g., pySmartDL missing).
            """
            task_info = None # Initialize return value

            # Check pySmartDL dependency only if not in dry run mode
            if not self._dryrun:
                try:
                    _import_pysmartdl()
                except ImportError as e:
                    self._print_locked(f"ERROR: Cannot add download task '{name}'. {e}", level=logging.ERROR)
                    # Set failure in results immediately
                    with self._state_lock:
                         self._final_results[name] = {
                             "type": "download", "url": url, "stdout": "",
                             "stderr": f"Failed to start: {e}", "returncode": -1,
                             "pid": None, "start_time": time.time(), "duration_sec": 0,
                             "filepath": None, "move_to": move_to, "dryrun": False,
                         }
                    return None # Indicate failure

            if not name:
                raise ValueError("Download 'name' required.")
            if not url:
                raise ValueError("Download 'url' required.")

            self._ensure_monitor_running()

            with self._state_lock:
                if name in self._active_tasks or name in self._final_results:
                    self._print_locked(
                        f"Warning: Task '{name}' exists. Skipping.", level=logging.WARNING
                    )
                    return None

                target_dir = directory or os.getcwd()
                initial_dest_path = target_dir # Let pySmartDL handle filename

                self._final_results[name] = {
                    "type": "download",
                    "stdout": "",
                    "stderr": "Submitted...",
                    "returncode": None,
                    "pid": None,
                    "start_time": None,
                    "duration_sec": None,
                    "url": url,
                    "filepath": None,
                    "move_to": move_to,
                    "dryrun": self._dryrun,
                }

                start_time = time.time()

                if self._dryrun:
                     self._print_status_block(
                        f"[DRYRUN] Task '{name}' (download)",
                        [f"URL: {url[:100]}{'...' if len(url) > 100 else ''}",
                         f"Target Dir: {target_dir}",
                         f"Move After: {move_to or 'No'}",
                         f"Simulating {DRY_RUN_SLEEP_DURATION}s execution..."]
                     )
                     if self._on_task_start:
                         try: self._on_task_start(name, "download", dryrun=True)
                         except Exception: pass

                     dry_run_completion_event = threading.Event()
                     timer = threading.Timer(DRY_RUN_SLEEP_DURATION, dry_run_completion_event.set)
                     timer.daemon = True
                     timer.start()

                     task_info = {
                        "type": "download",
                        "name": name,
                        "process": None,
                        "thread": None, # No real thread
                        "pid": None,
                        "output_queue": None,
                        "stream_reader_threads": [],
                        "start_time": start_time,
                        "final_output": {"stdout": [f"[DRYRUN] Would download {url}\n"], "stderr": []},
                        "task_status_code": 0,
                        "final_filepath": os.path.join(target_dir, f"simulated_{name}.file"), # Dummy path
                        "move_to_request": move_to,
                        "dryrun": True,
                        "dryrun_completion_event": dry_run_completion_event,
                        "dryrun_timer": timer,
                     }
                     self._active_tasks[name] = task_info
                     self._final_results[name].update({
                         "start_time": start_time,
                         "stderr": "",
                         "stdout": f"[DRYRUN] Would download {url}\n",
                         "filepath": task_info["final_filepath"], # Store dummy path
                     })

                else: # Real download
                    try:
                        output_q = queue.Queue()
                        dl_thread = threading.Thread(
                            target=RapidInstaller._execute_download_pysmartdl,
                            args=(url, initial_dest_path, output_q, name, self._verbose),
                            daemon=True,
                        )
                        dl_thread.start()
                        self._print_status_block(
                            f"STARTED Download '{name}'",
                            [f"URL: {url[:100]}{'...' if len(url) > 100 else ''}",
                             f"Target Dir: {target_dir}",
                             f"Move After: {move_to or 'No'}"]
                        )
                        if self._on_task_start:
                            try: self._on_task_start(name, "download", dryrun=False)
                            except Exception: pass

                        task_info = {
                            "type": "download",
                            "name": name,
                            "process": None,
                            "thread": dl_thread, # Real download thread
                            "pid": None,
                            "output_queue": output_q,
                            "stream_reader_threads": [],
                            "start_time": start_time,
                            "final_output": {"stdout": [], "stderr": []},
                            "task_status_code": None,
                            "final_filepath": None,
                            "move_to_request": move_to,
                            "dryrun": False,
                        }
                        self._active_tasks[name] = task_info
                        self._final_results[name].update(
                            {"start_time": start_time, "stderr": ""}
                        )

                    except Exception as e:
                        err_msg = f"ERROR starting download '{name}': {e}"
                        self._print_locked(f"  {err_msg}", level=logging.ERROR)
                        self._final_results[name].update(
                            {"stderr": err_msg, "returncode": -1, "start_time": start_time}
                        )
                        if name in self._active_tasks: del self._active_tasks[name]
                        return None # Indicate failure

            return task_info # Return tracking info

    # --- Core Monitoring Logic ---
    def _monitor_loop(self):
        self._monitor_thread_started.set()
        try:
            last_status_print_time = 0
            cycle_count = 0

            while not self._stop_monitor_event.is_set():
                if self._interrupt_received:
                    self._print_locked("Interrupt detected, exiting monitor...")
                    break

                cycle_start_time = time.time()
                cycle_count += 1

                output_collected_this_cycle = {}
                finished_tasks_in_cycle = []

                with self._state_lock:
                    active_tasks_snapshot = list(self._active_tasks.items())

                    if not active_tasks_snapshot and not self._stop_monitor_event.is_set():
                        # Check if pip resolution is pending before exiting
                        if not self._pip_tasks or self._pip_resolution_done:
                                self._print_locked("No active tasks remain, monitor thread exiting")
                                break
                        else:
                                # Pip tasks exist but haven't been resolved yet (wait() wasn't called)
                                # Monitor should wait until wait() triggers resolution or shutdown happens
                                pass # Continue loop, wait for wait() or shutdown()

                    for task_name, _ in active_tasks_snapshot:
                        output_collected_this_cycle[task_name] = {"stdout": [], "stderr": []}

                    for task_name, task_data in active_tasks_snapshot:
                        is_dryrun_task = task_data.get("dryrun", False)
                        is_finished = False
                        final_rc = None
                        completion_event = None

                        # Check if task is finished
                        if is_dryrun_task:
                            completion_event = task_data.get("dryrun_completion_event")
                            if completion_event and completion_event.is_set():
                                is_finished = True
                                final_rc = task_data.get("task_status_code", 0) # Default 0 for dry run
                        else: # Real task
                            if task_data["type"] == "command":
                                process = task_data["process"]
                                rc = process.poll()
                                if rc is not None:
                                    is_finished = True
                                    final_rc = rc
                            elif task_data["type"] == "download":
                                thread = task_data["thread"]
                                if not thread.is_alive():
                                    is_finished = True
                                    # Get status code from queue or default to 1 if missing
                                    final_rc = task_data.get("task_status_code", 1 if not task_data.get('dryrun') else 0)


                        # Process output queue (only for real tasks)
                        if not is_dryrun_task and task_data.get("output_queue"):
                                q = task_data["output_queue"]
                                try:
                                    while not q.empty():
                                        item = q.get_nowait()
                                        stream_name, content = item if isinstance(item, tuple) and len(item) == 2 else (None, None)

                                        if stream_name == TASK_STATUS_SENTINEL:
                                            # Special handling for download task status
                                            rc_dl, path = content if isinstance(content, tuple) else (content, None)
                                            task_data["task_status_code"] = rc_dl
                                            task_data["final_filepath"] = path
                                            if is_finished and final_rc is None: # Update final_rc if download thread finished before status arrived
                                                final_rc = rc_dl
                                            continue
                                        elif content is None and stream_name is not None: # Reader sentinel
                                            #print(f"DEBUG: Reader sentinel received for {task_name} stream {stream_name}")
                                            continue
                                        elif stream_name in ["stdout", "stderr"]:
                                            # Check for progress messages etc.
                                            if stream_name == "stdout" and isinstance(content, str) and "PROGRESS:" in content:
                                                progress_info = content.split("PROGRESS:", 1)[1].strip()
                                                task_data["download_progress"] = progress_info
                                                # Still store the raw message
                                                task_data["final_output"][stream_name].append(content)
                                                output_collected_this_cycle[task_name][stream_name].append(content)
                                            else:
                                                # Normal output
                                                task_data["final_output"][stream_name].append(content)
                                                output_collected_this_cycle[task_name][stream_name].append(content)
                                        #else:
                                            #print(f"DEBUG: Ignoring unexpected queue item for {task_name}: {item}")

                                except queue.Empty:
                                    pass
                                except Exception as e:
                                    self._print_locked(f"Error processing queue for {task_name}: {e}", level=logging.ERROR)

                        # --- Process Finished Task ---
                        if is_finished:
                            end_time = time.time()
                            start_time = task_data.get("start_time")
                            duration = (end_time - start_time) if start_time else None

                            # Final drain for real tasks
                            if not is_dryrun_task and task_data.get("output_queue"):
                                    q = task_data["output_queue"]
                                    try:
                                        while not q.empty():
                                            # Simplified drain, just get content
                                            stream_name, content = q.get_nowait()
                                            if stream_name == TASK_STATUS_SENTINEL:
                                                rc_dl, path = content if isinstance(content, tuple) else (content, None)
                                                final_rc = rc_dl if rc_dl is not None else final_rc # Prioritize status sentinel RC
                                                task_data["final_filepath"] = path if path else task_data.get("final_filepath")
                                            elif content is not None and stream_name in ["stdout", "stderr"]:
                                                task_data["final_output"][stream_name].append(content)
                                    except Exception: pass # Ignore errors during final drain


                            final_stdout_list = task_data["final_output"]["stdout"]
                            final_stderr_list = task_data["final_output"]["stderr"]
                            final_stdout = self._strip_ansi("".join(map(str, final_stdout_list)))
                            final_stderr = self._strip_ansi("".join(map(str, final_stderr_list)))


                            final_filepath_dl = task_data.get("final_filepath")

                            # Update final results
                            if task_name in self._final_results:
                                self._final_results[task_name].update({
                                    "stdout": final_stdout,
                                    "stderr": final_stderr,
                                    "returncode": final_rc,
                                    "duration_sec": duration,
                                    "filepath": final_filepath_dl, # Already set for dryrun, updated for download
                                })
                                # Schedule move only for successful, real downloads with a request
                                if final_rc == 0 and not is_dryrun_task and task_data['type'] == 'download':
                                    move_request = task_data.get("move_to_request")
                                    if move_request and final_filepath_dl:
                                            # Check if already added to avoid duplicates if monitor cycles fast
                                            if not any(m['task_name'] == task_name for m in self._deferred_moves):
                                                self._deferred_moves.append({
                                                    "task_name": task_name,
                                                    "src": final_filepath_dl,
                                                    "dest_dir": move_request,
                                                })
                            else:
                                self._print_locked(f"Warning: Task '{task_name}' finished but not in results", level=logging.WARNING)

                            # Call completion callback (add dryrun flag)
                            if self._on_task_complete:
                                try:
                                    self._on_task_complete(task_name, self._final_results.get(task_name, {}), dryrun=is_dryrun_task)
                                except Exception as e:
                                    self._print_locked(f"Error in on_task_complete callback for {task_name}: {e}", level=logging.WARNING)


                            # Record for finished task summary
                            finished_tasks_in_cycle.append({
                                "name": task_name, "returncode": final_rc, "duration": duration, "dryrun": is_dryrun_task
                            })

                            # Format completion message
                            status = "SUCCESS" if final_rc == 0 else f"FAILED (code {final_rc})"
                            duration_str = f"{duration:.2f}s" if duration is not None else "unknown time"
                            dryrun_tag = "[DRYRUN] " if is_dryrun_task else ""
                            completion_lines = [f"{dryrun_tag}Status: {status} in {duration_str}"]

                            # Add logs only for non-dryrun tasks
                            if not is_dryrun_task:
                                # Add stdout/stderr summary... (logic unchanged)
                                if final_stdout.strip():
                                    stdout_lines = final_stdout.strip().splitlines()
                                    limit = 10
                                    prefix = f"Log (last {limit} lines):" if len(stdout_lines) > limit else "Log:"
                                    displayed_stdout = "\n".join(stdout_lines[-limit:])
                                    completion_lines.extend([prefix, displayed_stdout])

                                if final_stderr.strip():
                                    stderr_lines = final_stderr.strip().splitlines()
                                    limit = 10
                                    prefix = f"Error Log (last {limit} lines):" if len(stderr_lines) > limit else "Error Log:"
                                    displayed_stderr = "\n".join(stderr_lines[-limit:])
                                    completion_lines.extend([prefix, displayed_stderr])


                            self._print_status_block(f"COMPLETED Task '{task_name}'", completion_lines)
                            del self._active_tasks[task_name]

                # --- Print Status Updates --- (outside the lock)
                if self._update_interval > 0 and (time.time() - last_status_print_time >= self._update_interval):
                    # Get a fresh snapshot of active tasks
                    with self._state_lock:
                            current_active_tasks = list(self._active_tasks.items())

                    if current_active_tasks:
                            status_lines = []
                            now = time.time()
                            for task_name, task_data in current_active_tasks:
                                start_time = task_data.get("start_time", 0)
                                duration = now - start_time if start_time else 0
                                is_dryrun_task = task_data.get("dryrun", False)
                                dryrun_tag = "[DRYRUN] " if is_dryrun_task else ""
                                task_type = task_data.get("type", "unknown")

                                if status_lines: status_lines.append("") # Separator
                                status_lines.append(f"{dryrun_tag}{task_name} ({task_type}) - Running for {duration:.1f}s")

                                if is_dryrun_task:
                                    status_lines.append("Status: Simulating...")
                                else:
                                    if task_type == "download":
                                            progress_info = task_data.get("download_progress", "Starting...")
                                            progress_parts = progress_info.split("|")
                                            progress_pct = progress_parts[0] if len(progress_parts) > 0 else "? %"
                                            speed = progress_parts[1] if len(progress_parts) > 1 else ""
                                            size = progress_parts[2] if len(progress_parts) > 2 else ""
                                            status_lines.append(f"Progress: {progress_pct}")
                                            if speed: status_lines.append(f"Speed: {speed}")
                                            if size: status_lines.append(f"Downloaded: {size}")
                                    elif task_type == "command":
                                            pid = task_data.get("pid", "N/A")
                                            status_lines.append(f"PID: {pid}")
                                            # Show recent output... (logic unchanged)
                                            recent_out = output_collected_this_cycle.get(task_name, {}).get("stdout", [])
                                            recent_err = output_collected_this_cycle.get(task_name, {}).get("stderr", [])
                                            out_text = self._process_status_lines(recent_out)
                                            err_text = self._process_status_lines(recent_err)
                                            if out_text:
                                                status_lines.append("Recent output:")
                                                status_lines.append(out_text[:200] + ("..." if len(out_text) > 200 else ""))
                                            if err_text:
                                                status_lines.append("Recent errors:")
                                                status_lines.append(err_text[:200] + ("..." if len(err_text) > 200 else ""))

                                self._print_status_block(f"Active Tasks Status @ {time.time():.1f}s", status_lines)
                                last_status_print_time = time.time()

                # Prevent CPU spinning
                time.sleep(0.1)

        except Exception as e:
            self._print_locked(f"MONITOR ERROR: {type(e).__name__}: {e}", level=logging.ERROR)
            import traceback
            self._print_locked(traceback.format_exc(), level=logging.ERROR)
        finally:
            self._print_locked("Monitor thread exiting")
            # Ensure state reflects monitor exit - might need cleanup?
            # Don't os._exit here, let wait() handle cleanup / exit codes
            # TODO
            #self._print_locked("Monitor thread exiting")
            self.shutdown(True)
            os._exit(130)

    # --- Deferred Move Logic ---
    def _perform_deferred_moves(self):
        """Moves downloaded files requested via 'move_to' after all tasks finish."""
        # Skip entirely in dry run mode
        if self._dryrun:
                if self._deferred_moves:
                    self._print_locked(f"\n{SEPARATOR}\n--- Deferred File Moves Skipped (Dry Run) ---")
                    for move_info in self._deferred_moves:
                        self._print_locked(f"[DRYRUN] Task '{move_info['task_name']}': Would move '{move_info['src']}' to '{move_info['dest_dir']}'")
                    self._print_locked(f"--- End Skipped Moves ---\n{SEPARATOR}\n")
                    self._deferred_moves = [] # Clear the list anyway
                return

        if not self._deferred_moves:
            return

        # ... (rest of move logic remains the same) ...
        self._print_locked(f"\n{SEPARATOR}\n--- Performing Deferred File Moves ---")
        moves_to_process = self._deferred_moves[:]
        self._deferred_moves = []

        for move_info in moves_to_process:
            task_name = move_info["task_name"]
            src_path = move_info["src"]
            dest_dir = move_info["dest_dir"]
            final_dest_path = None

            try:
                if not os.path.exists(src_path):
                    self._print_locked(f"[{task_name}] ERROR: Source file '{src_path}' not found for move.", level=logging.ERROR)
                    with self._state_lock:
                        if task_name in self._final_results: self._final_results[task_name]["move_status"] = "Error: Source not found"
                    continue

                os.makedirs(dest_dir, exist_ok=True)
                dest_filename = os.path.basename(src_path)
                final_dest_path = os.path.join(dest_dir, dest_filename)
                self._print_locked(f"[{task_name}] Moving '{src_path}' to '{final_dest_path}'...")
                shutil.move(src_path, final_dest_path)
                self._print_locked(f"[{task_name}] Move successful.")

                with self._state_lock:
                    if task_name in self._final_results:
                        self._final_results[task_name]["filepath"] = final_dest_path
                        self._final_results[task_name]["move_status"] = "Moved successfully"

            except OSError as e:
                self._print_locked(f"[{task_name}] ERROR moving file to '{dest_dir}': {e}", level=logging.ERROR)
                with self._state_lock:
                    if task_name in self._final_results: self._final_results[task_name]["move_status"] = f"Error: {e}"
            except Exception as e:
                self._print_locked(f"[{task_name}] UNEXPECTED ERROR during move: {e}", level=logging.ERROR)
                with self._state_lock:
                        if task_name in self._final_results: self._final_results[task_name]["move_status"] = f"Unexpected Error: {e}"

        self._print_locked(f"--- Finished Deferred File Moves ---\n{SEPARATOR}\n")


    # --- Public Control Methods ---
    def wait(self) -> Dict[str, Dict[str, Any]]:
        """
        Waits for all tasks (including pip installs if queued) to complete,
        performs deferred moves, and returns results.
        """
        pip_success = True
        # Check and run pip installs first if they haven't been run yet
        # Need lock to safely check/modify pip state flags
        run_pip = False
        with self._state_lock:
                if not self._pip_resolution_done and self._pip_tasks:
                    run_pip = True

        if run_pip:
                # Run pip installs *outside* the main state lock as it's blocking and calls add_task
                pip_success = self.pip_check_dependencies_and_install()
                if not pip_success:
                    self._print_locked("Pip installation process failed. See logs above.", level=logging.ERROR)
                    # Note: We still proceed to wait for other tasks

        # Now wait for the main monitor loop to finish all other tasks
        try:
            # Ensure monitor is running if tasks were added, even if pip failed
            self._ensure_monitor_running()

            if self._monitor_thread and self._monitor_thread.is_alive():
                    # Don't join with indefinite timeout if interrupt is possible
                    while self._monitor_thread.is_alive():
                        if self._interrupt_received:
                            print("\nInterrupt detected during wait(). Shutting down monitor...", file=sys.stderr)
                            self._stop_monitor_event.set()
                            # Give monitor a moment to exit gracefully
                            self._monitor_thread.join(timeout=2)
                            break
                        self._monitor_thread.join(timeout=0.1) # Non-blocking join check
            # Perform moves after monitor finishes
            self._perform_deferred_moves()

        except KeyboardInterrupt:
            print("\nKeyboard interrupt during wait(). Shutting down...", file=sys.stderr)
            return self.shutdown(terminate_processes=True) # shutdown handles exit

        finally:
                # Ensure shutdown logic runs even if monitor finished normally
                # This prints the final summary. Use terminate=False if we don't want to kill
                # potentially orphaned processes if the monitor died unexpectedly.
                if self._instance_active: # Only call shutdown if not already called
                    self.shutdown(terminate_processes=False) # Don't terminate here, should be done

        # Return final results collected by shutdown/monitor
        return self._final_results


    def shutdown(self, terminate_processes: bool = False):
        """
        Gracefully stop monitoring, optionally terminate subprocesses, and print summary.
        """
        if not self._instance_active:
            # Return results collected so far if shutdown called multiple times
            return self._final_results

        self._instance_active = False # Mark instance as shutting down
        self._stop_monitor_event.set() # Signal monitor thread to stop

        # Stop any active dry run timers
        with self._state_lock:
            for task_data in self._active_tasks.values():
                if task_data.get('dryrun') and task_data.get('dryrun_timer'):
                    task_data['dryrun_timer'].cancel()

        # Terminate real processes if requested
        if terminate_processes and not self._dryrun:
                terminated_tasks = []
                with self._state_lock:
                    for task_name, task_data in list(self._active_tasks.items()):
                        if task_data["type"] == "command" and task_data.get("process"):
                            pid = task_data['process'].pid
                            self._print_locked(f"Terminating process {pid} for task '{task_name}'...")
                            try:
                                # Send SIGTERM first (more graceful)
                                # Use os.killpg on Unix-like systems if start_new_session=True was used
                                if hasattr(os, "killpg") and hasattr(os, "getpgid"):
                                    os.killpg(os.getpgid(pid), signal.SIGTERM)
                                else:
                                    task_data["process"].terminate()
                                terminated_tasks.append(task_name)
                                # Update result immediately
                                if task_name in self._final_results:
                                    self._final_results[task_name].update({
                                        "returncode": -signal.SIGTERM, # Indicate termination signal
                                        "terminated": True,
                                        "stderr": self._final_results[task_name].get("stderr", "") +
                                                "\nProcess terminated by shutdown."
                                    })
                            except ProcessLookupError:
                                self._print_locked(f"Process {pid} for {task_name} already finished.")
                            except Exception as e:
                                self._print_locked(f"Error terminating {task_name} (PID {pid}): {e}")

                # Allow a brief moment for processes to terminate
                if terminated_tasks:
                    time.sleep(0.5)
                    # Optional: Force kill (SIGKILL) if still running - more aggressive
                    # with self._state_lock: ... check poll() again, use process.kill() ...

        # Wait briefly for the monitor thread to finish processing any final updates
        if self._monitor_thread and self._monitor_thread.is_alive():
                self._monitor_thread.join(timeout=1.0)

        # Perform final moves (already checks for dry run)
        self._perform_deferred_moves()

        # Print final summary
        with self._state_lock: # Access final results safely
                dry_run_msg = " (Dry Run)" if self._dryrun else ""
                total = len(self._final_results)
                # Count success/failure carefully, considering None return code as pending/failed
                # Treat terminated tasks as failed for summary purposes
                success_count = sum(1 for r in self._final_results.values() if r.get('returncode') == 0)
                failed_count = sum(1 for r in self._final_results.values() if r.get('returncode') is None or r.get('returncode') != 0)

                self._print_status_block(f"RapidInstall Run Complete{dry_run_msg}",
                                    [f"Total tasks processed: {total}",
                                        f"Successful: {success_count}",
                                        f"Failed/Terminated: {failed_count}"])

        # Remove temporary logger handler to prevent resource leaks if instance reused (though not typical)
        if self._logger and self._logger.handlers:
                self._logger.handlers.clear()

        return self._final_results

    # ... (shutdown, get_results unchanged) ...

    # Clarify 'run' method's scope
    def run(self, todos: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        DEPRECATED/LIMITED: Use install() function or class methods (add_task/add_download) directly.

        Processes tasks from a 'todos' list (supports 'commands' or 'download' keys)
        and waits for completion. Less explicit than using dedicated methods.
        """
        self._print_locked(
            "Warning: The run() method is less explicit than install() or add_task/add_download. Consider refactoring.",
            file=sys.stderr,
        )
        try:
            # Logic to handle mixed types from list (similar to standalone run_tasks)
            has_download = any("download" in todo for todo in todos)
            if has_download:
                _import_pysmartdl()  # Check dependency if needed

            tasks_added = set()
            for todo in todos:
                name = todo.get("name")
                if not name:
                    continue  # Skip unnamed
                if name in tasks_added:
                    continue  # Skip duplicate names in list

                if "commands" in todo and todo.get("commands"):
                    self.add_task(name=name, commands=todo["commands"])
                    tasks_added.add(name)
                elif "download" in todo and todo.get("download"):
                    # Extract move_to if present in the todo dict
                    self.add_download(
                        name=name,
                        url=todo["download"],
                        directory=todo.get("directory"),
                        move_to=todo.get("move_to"),
                    )
                    tasks_added.add(name)
        except ImportError as e:
            self._print_locked(f"ERROR: {e}", file=sys.stderr)
            raise e
        except (ValueError, RuntimeError) as e:
            self._print_locked(f"ERROR adding tasks in run(): {e}", file=sys.stderr)
        except Exception as e:
            self._print_locked(
                f"UNEXPECTED ERROR adding tasks in run(): {e}", file=sys.stderr
            )

        return self.wait()  # Waits for *all* tasks added to this instance

    def _parse_pip_report(self, report_path: str) -> Tuple[Dict[str, Dict], Dict[str, List[str]]]:
        """Parses the JSON report from 'pip install --report'."""
        installed_packages = {}
        dependencies = defaultdict(list)
        try:
            with open(report_path, 'r') as f:
                report = json.load(f)

            if 'install' not in report:
                self._print_locked(f"Warning: 'install' section not found in pip report {report_path}", level=logging.WARNING)
                return installed_packages, dependencies

            for item in report['install']:
                metadata = item.get('metadata', {})
                name = metadata.get('name')
                version = metadata.get('version')
                if not name or not version:
                    continue

                # Normalize name (e.g., replace underscores)
                norm_name = name.lower().replace('_', '-')

                installed_packages[norm_name] = {'name': name, 'version': version}

                # Extract dependencies
                requires_dist = metadata.get('requires_dist', [])
                if requires_dist:
                    for req in requires_dist:
                        # Basic parsing: take the part before semicolon, space, or bracket
                        dep_name_match = re.match(r"^[a-zA-Z0-9._-]+", req)
                        if dep_name_match:
                                dep_name = dep_name_match.group(0).lower().replace('_', '-')
                                # Ensure the dependency is also in our target install list
                                # This avoids adding dependencies outside the scope of the report
                                dependencies[norm_name].append(dep_name)

        except json.JSONDecodeError:
            self._print_locked(f"ERROR: Failed to parse pip report JSON: {report_path}", level=logging.ERROR)
            raise ValueError("Invalid pip report format")
        except Exception as e:
            self._print_locked(f"ERROR: Unexpected error parsing pip report {report_path}: {e}", level=logging.ERROR)
            raise

        # Filter dependencies to only include packages that are actually in the report's install list
        filtered_dependencies = defaultdict(list)
        installed_keys = set(installed_packages.keys())
        for pkg, deps in dependencies.items():
            if pkg in installed_keys:
                filtered_dependencies[pkg] = [dep for dep in deps if dep in installed_keys]

        return installed_packages, filtered_dependencies

    def _topological_sort(self, dependencies: Dict[str, List[str]], packages: Set[str]) -> List[List[str]]:
        """Performs topological sort to determine installation layers."""
        in_degree = {pkg: 0 for pkg in packages}
        adj = defaultdict(list) # Stores dependents: adj[dep] = [pkg1, pkg2] means pkg1, pkg2 depend on dep

        for pkg, deps in dependencies.items():
            for dep in deps:
                if dep in packages and pkg in packages: # Ensure both are in scope
                    adj[dep].append(pkg)
                    in_degree[pkg] += 1

        # Queue of packages with no prerequisites
        queue = deque([pkg for pkg in packages if in_degree[pkg] == 0])
        layers = []
        processed_count = 0

        while queue:
            current_layer = sorted(list(queue)) # Sort for deterministic order
            layers.append(current_layer)
            processed_count += len(current_layer)
            next_queue = deque()

            for pkg in current_layer:
                for dependent in adj[pkg]:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        next_queue.append(dependent)
            queue = next_queue

        if processed_count != len(packages):
            # Find cycles for better error message
            cycles = []
            involved_nodes = {pkg for pkg, degree in in_degree.items() if degree > 0}
            # Simple cycle detection might be complex; report nodes involved
            self._print_locked(f"ERROR: Cycle detected in pip dependencies involving: {involved_nodes}", level=logging.ERROR)
            raise RuntimeError("Cycle detected in package dependencies")

        return layers

    def pip_check_dependencies_and_install(self) -> bool:
        """
        Resolves pip dependencies for all queued requests and installs them in layers.
        This method is BLOCKING.

        Returns:
            True if all pip installations were successful, False otherwise.
        """
        with self._state_lock:
            if self._pip_resolution_done:
                return not self._pip_install_failed
            if not self._pip_tasks:
                self._pip_resolution_done = True
                return True # Nothing to do

            # Indicate start of pip phase
            self._print_locked(f"\n{SEPARATOR}\n--- Starting Pip Dependency Resolution and Installation ---")

            # --- Dry Run Simulation ---
            if self._dryrun:
                self._print_locked("[DRYRUN] Simulating pip dependency resolution...")
                all_packages_str = " ".join(p for task in self._pip_tasks for p in task[0])
                self._print_locked(f"[DRYRUN] Would analyze packages: {all_packages_str[:150]}{'...' if len(all_packages_str) > 150 else ''}")
                time.sleep(2) # Simulate resolution time
                self._print_locked("[DRYRUN] Simulating layered installation...")
                # Simulate a few layers
                for i in range(3):
                        self._print_locked(f"[DRYRUN] Simulating install of Layer {i}...")
                        time.sleep(1)
                self._print_locked("[DRYRUN] Pip installation simulation complete.")
                self._print_locked(f"--- Pip Phase Simulation Finished ---\n{SEPARATOR}\n")
                self._pip_resolution_done = True
                self._pip_install_failed = False # Assume success in dry run
                return True
            # --- End Dry Run Simulation ---

            # --- Real Pip Execution ---
            aggregated_packages = set()
            final_pip_options = []
            seen_options = set()
            master_index_url = None
            extra_index_urls = set()
            upgrade_all = False

            # Aggregate packages and options
            for packages, options in self._pip_tasks:
                aggregated_packages.update(packages)
                upgrade_all = upgrade_all or options.get('upgrade', False)
                if options.get('index_url'):
                    if master_index_url and master_index_url != options['index_url']:
                            self._print_locked(f"Warning: Multiple different --index-url specified. Using last one: {options['index_url']}", level=logging.WARNING)
                    master_index_url = options['index_url']
                extra_index_urls.update(options.get('extra_index_urls', []))
                for arg in options.get('additional_args', []):
                    if arg not in seen_options:
                        final_pip_options.append(arg)
                        seen_options.add(arg)

            if not aggregated_packages:
                self._print_locked("No pip packages to install after aggregation.", level=logging.INFO)
                self._pip_resolution_done = True
                return True

            # Construct pip command parts
            base_pip_cmd = [sys.executable, "-m", "pip", "install", "--dry-run"]
            if upgrade_all:
                base_pip_cmd.append("--upgrade")
            if master_index_url:
                base_pip_cmd.extend(["--index-url", master_index_url])
            for url in sorted(list(extra_index_urls)): # Sort for consistency
                base_pip_cmd.extend(["--extra-index-url", url])
            base_pip_cmd.extend(final_pip_options) # Add other args like --no-cache-dir

            # Create command for report generation
            report_cmd = base_pip_cmd[:]
            report_file = None
            try:
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".json", prefix="pip_report_") as tmp_report:
                    report_file = tmp_report.name
                report_cmd.extend(["--report", report_file])
                report_cmd.extend(list(aggregated_packages)) # Add actual packages

                self._print_locked("Running pip dependency resolution...")
                self._print_locked(f"Command: {' '.join(report_cmd)}") # Log the command

                # Execute pip --dry-run --report
                # Increase timeout for potentially complex resolutions
                process = subprocess.run(report_cmd, capture_output=True, text=True, timeout=300)

                if process.returncode != 0:
                    self._print_locked("ERROR: pip dependency resolution failed.", level=logging.ERROR)
                    self._print_locked("Pip Stdout:", level=logging.ERROR)
                    self._print_locked(process.stdout, level=logging.ERROR)
                    self._print_locked("Pip Stderr:", level=logging.ERROR)
                    self._print_locked(process.stderr, level=logging.ERROR)
                    self._pip_install_failed = True
                    self._pip_resolution_done = True
                    return False
                else:
                        self._print_locked("Pip dependency resolution successful.")
                        if process.stdout: self._print_locked("Pip Output:\n" + process.stdout) # Show output even on success
                        if process.stderr: self._print_locked("Pip Warnings/Messages:\n" + process.stderr)


                # Parse the report
                self._print_locked(f"Parsing pip report: {report_file}")
                installed_packages_info, dependencies = self._parse_pip_report(report_file)
                target_packages = set(installed_packages_info.keys()) # Get normalized names
                self._print_locked(f"Resolved {len(target_packages)} packages including dependencies.")

                # Perform topological sort
                layers = self._topological_sort(dependencies, target_packages)
                self._print_locked(f"Determined {len(layers)} installation layer(s).")

            except (ValueError, RuntimeError, subprocess.TimeoutExpired) as e:
                    self._print_locked(f"ERROR during pip setup: {e}", level=logging.ERROR)
                    self._pip_install_failed = True
                    self._pip_resolution_done = True
                    return False
            except Exception as e:
                    self._print_locked(f"UNEXPECTED ERROR during pip setup: {type(e).__name__}: {e}", level=logging.ERROR)
                    self._pip_install_failed = True
                    self._pip_resolution_done = True
                    return False
            finally:
                # Clean up report file
                if report_file and os.path.exists(report_file):
                    try:
                        os.remove(report_file)
                    except OSError:
                        self._print_locked(f"Warning: Could not remove temp report file {report_file}", level=logging.WARNING)

            # --- Execute Layers ---
            # Options for individual installs (no --upgrade here unless globally set)
            install_options = [sys.executable, "-m", "pip", "install", "--no-deps"]
            if master_index_url:
                install_options.extend(["--index-url", master_index_url])
            for url in sorted(list(extra_index_urls)):
                install_options.extend(["--extra-index-url", url])
            # Include options like --no-cache-dir etc. passed originally
            install_options.extend(final_pip_options)

            # Drop options not valid for single install like --upgrade (unless forced) or --dry-run
            install_options = [opt for opt in install_options if opt not in ["--dry-run", "--report"]]
            if upgrade_all:
                install_options.append("--upgrade") # Apply upgrade if globally requested

            # Release the state lock while running layers, as add_task needs it
            # The _pip_resolution_done flag prevents new pip tasks being added concurrently
            self._pip_resolution_done = True # Mark resolution as done *before* starting installs

        # <<< State lock released here >>>

        layer_success = True
        for i, layer in enumerate(layers):
            self._print_locked(f"\n--- Starting Pip Install Layer {i} ({len(layer)} packages) ---")
            layer_tasks = {} # Store {task_name: task_info} for this layer

            # Add tasks for the current layer
            for norm_pkg_name in layer:
                pkg_info = installed_packages_info[norm_pkg_name]
                pkg_name = pkg_info['name']
                pkg_version = pkg_info['version']
                pkg_spec = f"{pkg_name}=={pkg_version}"
                task_name = f"pip-install: {pkg_spec}"

                install_cmd_parts = install_options + [pkg_spec]
                install_cmd_str = " ".join(install_cmd_parts)

                # Add the task - add_task will acquire the lock briefly
                task_info = self.add_task(name=task_name, commands=install_cmd_str)
                if task_info:
                    layer_tasks[task_name] = task_info
                else:
                    # Failed to even add the task (e.g., duplicate name somehow?)
                    self._print_locked(f"ERROR: Failed to submit install task for {pkg_spec}", level=logging.ERROR)
                    layer_success = False
                    break # Fail the layer immediately

            if not layer_success: break # Stop processing layers

            # Wait for this layer's tasks to complete (blocking)
            self._print_locked(f"Waiting for Layer {i} tasks to complete...")
            active_layer_processes = {
                name: info['process'] for name, info in layer_tasks.items() if info and info['process']
            }
            completed_in_layer = set()
            while len(completed_in_layer) < len(active_layer_processes):
                time.sleep(0.2) # Check frequently but don't spin CPU
                for name, process in active_layer_processes.items():
                    if name in completed_in_layer:
                        continue
                    if process.poll() is not None:
                        completed_in_layer.add(name)
                        # Final status/output is handled by the main monitor loop shortly after
            self._print_locked(f"Layer {i} tasks finished execution.")

            # Check results for the layer (accessing _final_results needs lock)
            with self._state_lock:
                for task_name in layer_tasks.keys():
                    result = self._final_results.get(task_name)
                    if not result or result.get('returncode') != 0:
                        failed_rc = result.get('returncode', 'N/A') if result else 'N/A'
                        self._print_locked(f"ERROR: Task '{task_name}' failed in Layer {i} (RC: {failed_rc}).", level=logging.ERROR)
                        # Optionally log stderr from the failed task
                        if result and result.get('stderr'):
                                self._print_locked(f"--- Failure Log ({task_name}) ---\n{result['stderr']}\n--- End Log ---", level=logging.ERROR)
                        layer_success = False
                        self._pip_install_failed = True # Set global failure flag

            if not layer_success:
                self._print_locked(f"--- Pip Install Layer {i} FAILED. Aborting further pip installs. ---", level=logging.ERROR)
                break # Stop processing layers
            else:
                self._print_locked(f"--- Pip Install Layer {i} COMPLETED Successfully ---")


        # --- Final Pip Status ---
        with self._state_lock: # Re-acquire lock for final status update
            if not layer_success:
                self._pip_install_failed = True
            final_status = "FAILED" if self._pip_install_failed else "COMPLETED Successfully"
            self._print_locked(f"--- Pip Installation Phase {final_status} ---\n{SEPARATOR}\n")
            return not self._pip_install_failed
        # <<< State lock released here >>>

# --- Standalone Function (Updated to include move_to) ---
def run_tasks(
    todos: List[Dict[str, Any]],
    update_interval: int = DEFAULT_STATUS_UPDATE_INTERVAL,
    verbose: bool = True,
    dryrun: bool = False, # Added dryrun parameter
) -> Dict[str, Dict[str, Any]]:
    """
    Runs tasks defined in the 'todos' list. Supports commands and downloads.
    Can simulate execution with dryrun=True.
    """
    # exit_on_interrupt=False because run_tasks handles the KeyboardInterrupt directly
    installer = RapidInstaller(
        update_interval=update_interval,
        verbose=verbose,
        exit_on_interrupt=False,
        dryrun=dryrun # Pass dryrun flag
    )
    final_results = {}
    tasks_added = set()

    try:
        # Dependency check only needed if not dryrun and downloads exist
        if not dryrun and any("download" in todo for todo in todos):
            _import_pysmartdl() # Check dependency

        for todo in todos:
            name = todo.get("name")
            if not name:
                print("Warning: Skipping task with no name.", file=sys.stderr)
                continue
            if name in tasks_added:
                print(f"Warning: Duplicate task name '{name}'. Skipping.", file=sys.stderr)
                continue

            task_info = None
            if "commands" in todo:
                commands = todo.get("commands")
                if commands:
                    task_info = installer.add_task(name=name, commands=commands)
                else:
                    print(f"Skipping command task '{name}' empty 'commands'.", file=sys.stderr)
            elif "download" in todo:
                url = todo.get("download")
                if url:
                    task_info = installer.add_download(
                        name=name, url=url,
                        directory=todo.get("directory"), move_to=todo.get("move_to")
                    )
                else:
                    print(f"Skipping download task '{name}' empty 'download' URL.", file=sys.stderr)
            # Pip tasks could theoretically be added via todos if structured correctly,
            # but the primary interface is installer.add_pip()
            elif "pip" in todo:
                 packages = todo.get("pip")
                 if packages:
                      installer.add_pip(
                          packages,
                          extra_index_urls=todo.get("extra_index_urls"),
                          upgrade=todo.get("upgrade", False),
                          pip_options=todo.get("pip_options")
                      )
                      # Note: pip tasks don't immediately add to tasks_added set in the same way
                 else:
                      print(f"Skipping pip task '{name}' empty 'pip' value.", file=sys.stderr)

            else:
                print(f"Skipping task '{name}': No 'commands', 'download', or 'pip'.", file=sys.stderr)

            if task_info: # If add_task/add_download returned info (meaning it was added)
                 tasks_added.add(name)


        final_results = installer.wait() # Wait handles pip install logic internally

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected in run_tasks. Shutting down...", file=sys.stderr)
        # shutdown returns the results collected up to the interrupt
        final_results = installer.shutdown(terminate_processes=True)
        # Explicitly exit for standalone function case after shutdown attempt
        print("Exiting due to user interrupt...", file=sys.stderr)
        sys.exit(130)
    except ImportError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        # Return whatever results were collected before the import error
        final_results = installer.shutdown(terminate_processes=False)
    except Exception as e:
        print(f"UNEXPECTED ERROR in run_tasks: {type(e).__name__}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        final_results = installer.shutdown(terminate_processes=True) # Terminate on unexpected errors

    return final_results
