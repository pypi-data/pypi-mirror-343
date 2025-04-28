"""Sphinx configuration for itango documentation."""

import os
import sys

# Extensions
sys.path.append(os.path.abspath("sphinxext"))
extensions = [
    "sphinx.ext.intersphinx",
    "ipython_console_highlighting",
    "tango_console_highlighting",
]

# Configuration
html_theme = "sphinx_book_theme"

html_title = "ITango"
html_theme_options = {
    "repository_url": "https://gitlab.com/tango-controls/itango",
    "path_to_docs": "doc",
    "repository_branch": "main",
    "use_source_button": True,
    "use_edit_page_button": True,
}

# The suffix of source filenames.
source_suffix = {
    ".rst": "restructuredtext",
}

master_doc = "index"
rst_epilog = """\
.. _Tango: http://www.tango-controls.org/
.. _IPython: http://ipython.org/
.. _ITango: https://pypi.python.org/pypi/itango/
"""

# Data

project = "itango"
copyright = "2016, Tango Controls"
author = "Tango Controls"


intersphinx_mapping = {
    "tango-controls": ("https://tango-controls.readthedocs.io/en/latest/", None),
    "pytango": ("https://pytango.readthedocs.io/en/stable/", None),
    "python": ("https://docs.python.org/3", None),
}
