# rapidinstall/__init__.py

# Import the class and the standalone function from run.py
from .run import RapidInstaller, run_tasks, DEFAULT_STATUS_UPDATE_INTERVAL

# Define the public API - the install function and the class

from typing import List, Dict, Any, Optional


def install(
    todos: List[Dict[str, Any]],
    update_interval: Optional[int] = None,
    verbose: bool = True,
) -> Dict[str, Dict[str, Any]]:
    """
    Runs a list of installation tasks (shell commands) in parallel using RapidInstaller.

    Provides real-time status updates and aggregated output.

    Example:
        import rapidinstall
        my_tasks = [
            {'name': 'task1', 'commands': 'echo "Hello"; sleep 2'},
            {'name': 'task2', 'commands': 'echo "World"; sleep 1'}
        ]
        # Using the function
        results_func = rapidinstall.install(my_tasks)
        print("Function Results:", results_func)

        # Using the class directly
        installer = rapidinstall.RapidInstaller(verbose=True)
        installer.add_task(name='task3', commands='echo "Classy"; sleep 1')
        installer.add_tasks(my_tasks) # Can add more
        results_class = installer.wait()
        print("Class Results:", results_class)


    Args:
        todos: List of task dictionaries [{'name': str, 'commands': str}, ...].
        update_interval (Optional[int]): Print status every N iterations.
                                         Defaults to DEFAULT_STATUS_UPDATE_INTERVAL.
                                         Set to 0 or None to disable.
        verbose (bool): Print progress and output to console. Defaults to True.

    Returns:
        Dict[str, Dict[str, Any]]: Dictionary mapping task names to results
                                   (stdout, stderr, returncode, pid).
    """
    # Use default from run module if not provided
    interval_to_use = (
        update_interval
        if update_interval is not None
        else DEFAULT_STATUS_UPDATE_INTERVAL
    )

    # Use the standalone run_tasks function which now internally uses the class
    # This maintains the simplest interface for the 'install' function.
    # Alternatively, you could instantiate RapidInstaller here:
    # installer = RapidInstaller(update_interval=interval_to_use, verbose=verbose)
    # return installer.run(todos)
    return run_tasks(todos=todos, update_interval=interval_to_use, verbose=verbose)


# Package version


__version__ = "1.2.2"  # Updated version for class refactor

# Control `from rapidinstall import *`


# Expose the main function, the class, and the standalone runner function
__all__ = ["install", "RapidInstaller", "run_tasks", "DEFAULT_STATUS_UPDATE_INTERVAL"]
