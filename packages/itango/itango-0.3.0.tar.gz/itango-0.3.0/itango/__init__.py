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

__all__ = [
    "install",
    "load_ipython_extension",
    "unload_ipython_extension",
    "init_ipython",
    "load_config",
    "run",
    "run_qt",
    "get_python_version",
    "get_ipython_version",
    "get_pytango_version",
]

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "0.0+unknown"

from .common import get_ipython_version, get_pytango_version, get_python_version
from .install import install
from .itango import (
    init_ipython,
    load_config,
    load_ipython_extension,
    run,
    run_qt,
    unload_ipython_extension,
)
