
Getting Started
===============

Python 3
^^^^^^^^

Make sure you have Python 3 installed. On Windows and OSX you can simply install
the latest Python 3 by downloading an installer from the official_ Python site.

.. Note:: We recommend Python 3.6 or higher because of general **speed improvements**
    of the language, but Python versions down to 3.4 should work.

Most linux distributions already have at least Python 3.4 installed thought `python3`.
See documentation for your distribution on how to install a newer versions.

It is common to have multiple versions of Python installed on all operating systems.

Create a virualenv
^^^^^^^^^^^^^^^^^^

First of all create a directory for your project and naviagate to it using a terminal.
We assume Python 3 here.

OS X / Linux

    python3.6 -m pip install virtualenv
    python3.6 -m virtualenv env

Windows

    python36.exe -m pip install virtualenv
    python36.exe -m virtualenv env


.. _official: https://www.python.org/
