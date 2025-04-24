import pytest
import sys
import os

from src.rapidinstall import RapidInstaller, install

#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


@pytest.fixture
def installer():
    return RapidInstaller(verbose=False)


@pytest.mark.parametrize(
    "command, expected_output",
    [
        ("echo Hello", "Hello"),
        ("echo World", "World"),
    ],
)
def test_add_and_run_command(installer, command, expected_output):
    installer.add_task(name=expected_output, commands=command)
    results = installer.wait()
    assert expected_output in results
    if results[expected_output]["returncode"] != 0:
        print("STDERR:", results[expected_output].get("stderr"))
    assert results[expected_output]["returncode"] == 0
    if expected_output not in results[expected_output]["stdout"]:
        print("FULL RESULTS:", results)
    assert expected_output in results[expected_output]["stdout"]


def test_error_command(installer):
    installer.add_task(name="fail", commands="exit 1")
    results = installer.wait()
    assert "fail" in results
    assert results["fail"]["returncode"] != 0


def test_install_function_runs_commands():
    todos = [
        {"name": "hello", "commands": "echo Hello"},
        {"name": "world", "commands": "echo World"},
    ]
    results = install(todos, update_interval=0, verbose=False)
    assert "hello" in results
    assert "world" in results
    assert results["hello"]["returncode"] == 0
    assert results["world"]["returncode"] == 0


def test_add_download_mocked(monkeypatch, installer):
    # Mock _import_pysmartdl to avoid real import
    monkeypatch.setattr("src.rapidinstall.run._import_pysmartdl", lambda: True)

    # Mock the download execution method
    def fake_download(url, dest, output_q, name, verbose):
        output_q.put(("_task_status", (0, "/fake/path/file.txt")))

    monkeypatch.setattr(
        "src.rapidinstall.run.RapidInstaller._execute_download_pysmartdl",
        staticmethod(fake_download),
    )

    installer.add_download(url="http://example.com/file", name="file_download")
    results = installer.wait()
    assert "file_download" in results
    assert results["file_download"]["returncode"] == 0
    assert results["file_download"]["filepath"] == "/fake/path/file.txt"


def test_task_stdout_stderr_capture(installer):
    cmd = (
        f"{sys.executable} -c "
        "\"import sys; print('hello stdout'); print('hello stderr', file=sys.stderr)\""
    )
    installer.add_task(name="stdout_stderr_test", commands=cmd)
    results = installer.wait()
    result = results.get("stdout_stderr_test")
    assert result is not None
    assert result["returncode"] == 0
    assert "hello stdout" in result["stdout"]
    assert "hello stderr" in result["stderr"]
