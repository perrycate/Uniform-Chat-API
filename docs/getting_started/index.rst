.. _getting_started:

Getting Started
******************************

Installation
==============================
You will need the following dependencies:

* Make
* Python3
* Pip3
* Pipenv (install with ``pip3 install pipenv``)

You can download Unichat here::

https://github.com/TheGuyWithTheFace/Uniform-Chat-API

From the base directory, run ``make install``.

.. Note::
    This will create a virtual environment (usually in
    ``~/.local/share/virtualenvs``) and install the other dependencies listed
    in ``Pipfile``. Because of the virtual environment, these dependencies will
    not be accessible to other programs. Also, when you run ``make`` or ``make
    serve``, the virtualenv will be used automatically, so you don't need to
    run anything other than ``make``.

Congratulations, you've installed Unichat!

Usage
==============================

To run the Unichat server, simply run ``make`` or ``make serve`` from the base
directory.

By default you can connect to the server on ``localhost:8000``.

Note that to make valid calls, most services will require you to acquire
authentication tokens and pass them as a GET request parameter by appending
``?token=<token here>`` to the url. For tutorials on how to acquire such tokens,
see :ref:`authentication`.
