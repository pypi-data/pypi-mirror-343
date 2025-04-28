# SPDX-FileCopyrightText: All Contributors to the ITango project
# SPDX-License-Identifier: LGPL-3.0-or-later

import contextlib
import os
import socket
import subprocess
import sys
import time
from unittest import mock

import pytest
import tango
from IPython.terminal.interactiveshell import TerminalInteractiveShell


def get_free_port():
    """Return a free port

    There is a race condition as another process could take
    the port after the function returns,
    but it's probably good enough.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind to a free port provided by the OS
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def mock_tango_host():
    """Mock TANGO_HOST env variable"""
    PYTANGO_HOST = f"127.0.0.1:{get_free_port()}"
    with mock.patch.dict(os.environ, {"TANGO_HOST": PYTANGO_HOST}):
        yield PYTANGO_HOST


@pytest.fixture(scope="session")
def pytango_db(mock_tango_host):
    """Start PyTango database and TangoTest"""
    # Copy env to inherit PATH
    # When passing env to subprocess, it fully replaces os.environ
    env = os.environ.copy()
    # Don't write to disk
    env["PYTANGO_DATABASE_NAME"] = ":memory:"
    try:
        databaseds = subprocess.Popen(
            [sys.executable, "-m", "tango.databaseds.database", "2"],
            stderr=subprocess.PIPE,
            env=env,
        )
        waited = 0
        dt = 0.3
        while True:
            time.sleep(dt)
            waited += dt
            if databaseds.poll() is not None:
                stderr = databaseds.stderr.read().decode()
                print("------------------STDERR------------------")
                print(stderr)
                print("------------------------------------------")
                raise RuntimeError(f"Database stopped: {databaseds.returncode}")
            try:
                host, port = mock_tango_host.split(":")
                db = tango.Database(host, int(port))
                db.get_info()
                break
            except tango.DevFailed as exc:
                if waited > 10:
                    raise RuntimeError(
                        f"Tired of waiting for database...{exc}"
                    ) from exc

        # Start TangoTest
        tango_test = subprocess.Popen(
            ["TangoTest", "test"],
            stderr=subprocess.PIPE,
        )
        waited = 0
        dt = 0.3
        while True:
            time.sleep(dt)
            waited += dt
            if tango_test.poll() is not None:
                stderr = tango_test.stderr.read().decode()
                print("------------------STDERR------------------")
                print(stderr)
                print("------------------------------------------")
                raise RuntimeError(f"TangoTest stopped: {tango_test.returncode}")
            try:
                proxy = tango.DeviceProxy(f"tango://{mock_tango_host}/sys/tg_test/1")
                proxy.ping()
                if proxy.read_attribute("State").value == tango.DevState.RUNNING:
                    break
            except tango.DevFailed as exc:
                if waited > 10:
                    raise RuntimeError(
                        f"Tired of waiting for device proxy...{exc}"
                    ) from exc

        yield mock_tango_host

    finally:
        # Clean up
        try:
            tango_test.kill()
        except Exception:
            pass
        with contextlib.suppress(Exception):
            databaseds.kill()


@pytest.fixture(scope="session")
def ipython_shell(pytango_db):
    # Create and return a fresh IPython shell instance
    shell = TerminalInteractiveShell.instance()
    shell.extension_manager.load_extension("itango")
    yield shell
