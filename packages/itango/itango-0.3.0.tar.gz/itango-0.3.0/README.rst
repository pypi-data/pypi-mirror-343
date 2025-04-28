ITango
======

An interactive Tango client.


Description
-----------

ITango_ is a PyTango_ CLI based on IPython_.
It is designed to be used as an IPython profile.

It is available since PyTango 7.1.2 and has been moved to a separate
project since PyTango 9.2.0.


Requirements
------------

ITango is compatible with python >= 3.9. It requires:

-  PyTango_ >= 9.3
-  IPython_ >= 8.5

See previous versions for older compatibility.


Install
-------

ITango is available on PyPI_::

    $ pip install itango         # latest version
    $ pip install itango[qt]     # to install qtconsole


Usage
-----

ITango can be started using the ``itango`` script::

    $ itango  # Or itango3 for backward compatibility

or the ``tango`` profile::

    $ ipython --profile=tango


Features
--------

ITango works like a normal python console, but it provides a nice set of
features from IPython:

-  proper (bash-like) command completion
-  automatic expansion of python variables, functions, types
-  command history (with up/down arrow keys, %hist command)
-  help system ( object? syntax, help(object))
-  persistently store your favorite variables
-  color modes

For a complete list checkout the `IPython web page`_.

It also adds set of PyTango_ specific features:

-  automatic import of Tango objects
-  device and attribute name completion
-  list tango devices, classes, servers
-  customized tango error message
-  database utilities

Check out the documentation_ for more informations.

.. _IPython: http://ipython.org/
.. _ITango: http://pypi.python.org/pypi/itango/
.. _PyTango: https://gitlab.com/tango-controls/pytango
.. _documentation: https://itango.readthedocs.io/

.. _PyPI: ITango_
.. _IPython web page: IPython_
