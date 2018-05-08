.. _introduction:

Introduction
*******************************

Unichat: The Universal Chat API
===============================

.. NOTE. FIXME: You need to sell this a bit more.

   "Unichat is a server designed to allow the transcripts for multiple social media
   chat to be consumed through a uniform API. Because none of these chat services
   have agreed on a standard, this project seeks to enable more convenient personal
   analytics for interpersonal conversations through a common interface. In
   particular: Queries to the unichat server follow the same API
   and return data in the same format regardless of the outgoing service."

Unichat is a server designed to allow querying multiple chat APIs at the same
time. Queries to the unichat server follow the same API and return data in the
same format regardless of the outgoing service.

Unichat's interface is:

 1. *Simple.* Only the bare minimum necessary is returned for each API call, so
    it's easy to learn and use quickly.
 2. *Uniform.* If you write something to interact with one service, it will work
    with any other supported service.
 3. *Well-documented.* Everything you need to use Unichat can be found on this
    site. Disagree? Raise an issue `here.
    <https://github.com/TheGuyWithTheFace/Uniform-Chat-API/issues>`_


Supported Services
==============================

As of 5/5/18, Unichat has full support for Slack and Groupme. Planned support
includes Discord and Facebook Messenger. More information on API compatibility
can be found in the :ref:`api reference`.


How it works
===============================

Clients send requests to the Unichat Server over HTTP, just like any other web
server. Unichat interprets that request, makes the equivalent request to the
external service, then translates the returned data back into a uniform format,
and returns it to the client.

For more information on the internals of how Unichat works, check out `the
GitHub repository <https://github.com/TheGuyWithTheFace/Uniform-Chat-API>`_, or
read over the section on :ref:`contributing`.


Example uses
===============================

Looking for ideas? Here are some data analysis questions Unichat can help
investigate:

* A script to download messages from any chat service.
* A program to see who is the most verbose in a chat.
* A tool to see the times of the day that a chat is most active.


How to read this document
===============================

The :ref:`getting_started` section contains all you need to install and run
Unichat. Once running, the Tutorials section has instructions for
:ref:`authentication` with various APIs. The :ref:`api reference` describes how
to use Unichat, including descriptions of each of the :ref:`endpoints`. Want to
learn more about how Unichat works? Look at :ref:`contributing`.
