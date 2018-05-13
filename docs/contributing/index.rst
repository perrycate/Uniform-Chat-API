.. _contributing:

How to Contribute
******************************

Unichat Architecture
==============================

Terminology
------------------------------
 * **Handler**: Handles all incoming HTTP requests for a particular resource,
   invoking the appropriate translator, and eventually returning the result in
   a uniform format.
 * **Translator**: Makes outgoing requests to a particular service.
 * **Service**: Any messaging API we can make outgoing queries against.

Relevant Files
------------------------------
 * ``sanity.py``: Basic tests to make sure the API isn't completely broken.
 * ``unichat/app.py``: Sets everything up. Configures handlers+endpoints, routes,
   errors, etc.
 * ``unichat/errors.py``: Maps raisable exceptions to error handling code.
 * ``unichat/models.py``: Defines basic data objects passed between handlers and
   translators.
 * ``unichat/util.py``: Contains various generically useful helper functions.
 * ``unichat/handlers.py``: Defines falcon resources for each endpoint. Handlers
   invoke the appropriate translator depending on the service requested.
 * ``unichat/translators/*``: Contains Translators to manage requests to various
   messaging APIs.

Testing
==============================

.. Note::
    Currently ``make test`` only runs a very basic test to see if the server
    returns an HTTP error for a valid request, with no other checks of any kind.

.. Warning::
    User must have Python 3, pip, and pipenv installed
    Before running tests. Modify test.config.sample (adding authentication tokens
    as necessary) and save it as test.congig. Otherwise, any tests requiring
    authentication will fail.

In one terminal::

    $ make install # (If this is the first time)
    $ make serve

In another::

    $ make test

Or, for more verbose output (such as the JSON returned from each request)::

    $ make test-verbose



How to give feedback
==============================

Find a bug? Have an enhancement idea? Open a GitHub issue `here.
<https://github.com/TheGuyWithTheFace/Uniform-Chat-API/issues>`_ Any and all
feedback is welcome!

