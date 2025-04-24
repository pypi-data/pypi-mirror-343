import sys
import os
import pytest
from unittest import mock

#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src.rapidinstall import RapidInstaller

@mock.patch("src.rapidinstall.run.pip_concurrent")
def test_add_pip_and_wait_single(mock_pip_concurrent):
    installer = RapidInstaller()
    installer.add_pip("packageA packageB")
    installer._monitor_thread = mock.Mock()
    installer._monitor_thread.join = mock.Mock()
    installer.wait()

    # Check concurrent_install called once with correct packages
    calls = mock_pip_concurrent.concurrent_install.call_args_list
    assert len(calls) == 1
    args, kwargs = calls[0]
    assert set(args[0]) == {"packageA", "packageB"}

@mock.patch("src.rapidinstall.run.pip_concurrent")
def test_add_pip_and_wait_multiple(mock_pip_concurrent):
    installer = RapidInstaller()
    installer.add_pip("packageA packageB")
    installer.add_pip("packageC packageD")
    installer._monitor_thread = mock.Mock()
    installer._monitor_thread.join = mock.Mock()
    installer.wait()

    # Check concurrent_install called twice with correct packages
    calls = mock_pip_concurrent.concurrent_install.call_args_list
    assert len(calls) == 2
    pkgs1 = set(calls[0][0][0])
    pkgs2 = set(calls[1][0][0])
    assert pkgs1 == {"packageA", "packageB"}
    assert pkgs2 == {"packageC", "packageD"}