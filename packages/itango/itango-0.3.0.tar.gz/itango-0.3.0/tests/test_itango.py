# SPDX-FileCopyrightText: All Contributors to the ITango project
# SPDX-License-Identifier: LGPL-3.0-or-later

import re

import tango
from IPython.utils.io import capture_output


def test_db_info(ipython_shell):
    # db variable contains Database
    with capture_output() as captured:
        result = ipython_shell.run_cell("print(db.get_info())")
    assert result.success
    assert "Running since" in captured.stdout
    assert "Devices defined =" in captured.stdout
    assert "Device servers exported =" in captured.stdout
    assert "Class properties defined =" in captured.stdout


def test_lsdev_magic(ipython_shell):
    with capture_output() as captured:
        result = ipython_shell.run_cell("lsdev")
    assert result.success
    assert result.result is None
    assert (
        re.search(r"sys/database/2\s*DataBaseds/2\s*DataBase", captured.stdout)
        is not None
    )
    assert (
        re.search(r"sys/tg_test/1\s*TangoTest/test\s*TangoTest", captured.stdout)
        is not None
    )


def test_lsdevclass_magic(ipython_shell):
    with capture_output() as captured:
        result = ipython_shell.run_cell("lsdevclass")
    assert result.success
    assert result.result is None
    assert "sys/database/2" not in captured.stdout
    assert "DataBase" in captured.stdout
    assert "TangoTest" in captured.stdout


def test_lsserv_magic(ipython_shell):
    with capture_output() as captured:
        result = ipython_shell.run_cell("lsserv")
    assert result.success
    assert result.result is None
    assert "sys/database/2" not in captured.stdout
    assert "DataBaseds/2" in captured.stdout
    assert "TangoTest/test" in captured.stdout


def test_device_proxy(ipython_shell):
    # DeviceProxy imported and available
    result = ipython_shell.run_cell("DeviceProxy('sys/tg_test/1').State()")
    assert result.success
    assert result.result == tango.DevState.RUNNING


def test_device(ipython_shell):
    # Device is equivalent to DeviceProxy
    result = ipython_shell.run_cell("Device('sys/tg_test/1').State()")
    assert result.success
    assert result.result == tango.DevState.RUNNING


def test_tango_test_class(ipython_shell):
    # TangoTest can be used as DeviceProxy
    result = ipython_shell.run_cell("TangoTest('sys/tg_test/1').Status()")
    assert result.success
    assert result.result == "The device is in RUNNING state."


def test_dev_not_found(ipython_shell):
    with capture_output() as captured:
        result = ipython_shell.run_cell("Device('sys/tg_test/2').state()")
    assert not result.success
    assert "device sys/tg_test/2 not defined in the database" in captured.stdout


def test_dev_not_exported(ipython_shell):
    with capture_output() as captured:
        result = ipython_shell.run_cell("Device('sys/access_control/1').state()")
    assert not result.success
    assert "Device sys/access_control/1 is not exported" in captured.stdout


def test_refreshdb_magic(ipython_shell):
    device_name = "sys/tg_test/2"
    # Add a new device to the database
    db = tango.Database()
    dev_info = tango.DbDevInfo()
    dev_info.name = device_name
    dev_info._class = "TangoTest"
    dev_info.server = "TangoTest/test"
    db.add_device(dev_info)
    try:
        # device was added after itango was loaded - it's not in cache
        with capture_output() as captured:
            ipython_shell.run_cell("lsdev")
        assert device_name not in captured.stdout
        # Run refreshdb
        ipython_shell.run_cell("refreshdb")
        # new device is now listed
        with capture_output() as captured:
            ipython_shell.run_cell("lsdev")
        assert device_name in captured.stdout
    finally:
        # Cleaning
        db.delete_device(device_name)
