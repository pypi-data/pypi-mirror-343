#!/usr/bin/env python

# -----------------------------------------------------------------------------
# This file is part of ITango (http://pypi.python.org/pypi/itango)
#
# Copyright 2006-2012 CELLS / ALBA Synchrotron, Bellaterra, Spain
# Copyright 2013-2014 European Synchrotron Radiation Facility, Grenoble, France
#
# Distributed under the terms of the GNU Lesser General Public License,
# either version 3 of the License, or (at your option) any later version.
# See LICENSE.txt for more info.
# -----------------------------------------------------------------------------

"""functions common (hopefully) to all ipython versions"""

__all__ = ["get_python_version", "get_ipython_version", "get_pytango_version"]

import sys
from importlib.metadata import version

from packaging.version import Version

# Python utilities


def get_python_version():
    return Version(".".join(map(str, sys.version_info[:3])))


# IPython utilities


def get_ipython_version():
    """Returns the current IPython version"""
    return Version(version("ipython"))


# PyTango utilities


def get_pytango_version():
    return Version(version("pytango"))
