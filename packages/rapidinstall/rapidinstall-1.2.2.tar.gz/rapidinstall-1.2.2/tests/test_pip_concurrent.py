import sys
import os
import pytest
from unittest import mock

#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src.rapidinstall import pip_concurrent

def fake_pip_show(package_name):
    """Simulate 'pip show' output for dependencies."""
    deps_map = {
        "A": "B, C",
        "B": "D",
        "C": "",
        "D": "",
    }
    deps = deps_map.get(package_name, "")
    output = f"Name: {package_name}\nRequires: {deps}\n"
    return mock.Mock(returncode=0, stdout=output)

def fake_pip_install(package_name):
    """Simulate 'pip install' command."""
    print(f"Mock install {package_name}")
    return mock.Mock(returncode=0)

@mock.patch("subprocess.run")
def test_concurrent_install(mock_run):
    def side_effect(cmd, *args, **kwargs):
        if cmd[:2] == ["pip", "show"]:
            pkg = cmd[2]
            return fake_pip_show(pkg)
        elif cmd[:2] == ["pip", "install"]:
            pkg = cmd[2]
            return fake_pip_install(pkg)
        else:
            return mock.DEFAULT

    mock_run.side_effect = side_effect

    packages = ["A"]
    pip_concurrent.concurrent_install(packages, max_workers=2)

    # Check that pip show and pip install were called for all packages
    called_pkgs = [call[0][0][2] for call in mock_run.call_args_list if call[0][0][:2] == ["pip", "install"]]
    assert set(called_pkgs) == {"A", "B", "C", "D"}