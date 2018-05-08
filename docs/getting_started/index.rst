.. _getting_started:

Getting Started
******************************

.. NOTE. It'd be great here if you explained what the moving parts are.
   It would be great if you explained what is being installed, how the
   user's system is modified, how to reverse everything.

   It is good to explain that a server will be listening on a port. It
   would be useful to mention what happens if that port is not free.
   (8000 is a port used by many things, so it would be great to...)
   
   FIXME: allow running on another port.

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

Congratulations, you've installed Unichat!

Usage
==============================

.. NOTE. What about pipenv? You cannot assum that the user knows this.
   You have to explain what it does, how it works, link to documentation,
   then you have to explain how to use it for the purpose of using your
   project.

To run the Unichat server, simply run ``make`` or ``make serve`` from the base
directory.

By default you can connect to the server on ``localhost:8000``.

Note that to make valid calls, most services will require you to acquire
authentication tokens and pass them as a GET request parameter. For tutorials
on how to acquire such tokens, see :ref:`authentication`.

.. NOTE. What about instructions on how to include the token? I added
   that it was through a GET parameter, but you should make it more detailed,
   I think, no?
