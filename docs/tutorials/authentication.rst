.. _authentication:

Authentication
==============================

Unichat interacts with various services on behalf of the client. Because of
this, clients must log in (or *authenticate*) with these other services first
before these services will respond with your messages.

Modern Authentication is almost always done through
`Oauth2 <https://oauth.net/2/>`_. After a client logs in, the server provides a
*token* (usually a string of some sort). On every request, the client must
include the provided token to prove to the server that the client is logged in.
Here are instructions for how to acquire these login tokens for each supported
(Tier 1 and above) service.

.. Note::
    In the future, Unichat will offer a uniform interface to programatically
    authenticate through, making this process unnecessary.

GroupMe Instructions
------------------------------
1. Log into ``dev.groupme.com``:

.. figure:: /screenshots/Screenshot_20180411_224924.png

2. Click "Access Token" in the upper right corner:

.. figure:: /screenshots/Screenshot_20180411_225501.png

3. You should see a popup with your API Access token. You're done!

Slack Instructions
------------------------------
1. Go to ``api.slack.com`` and click "Start Building":

.. figure:: /screenshots/Screenshot_20180411_231758.png

2. Enter an app name and select a workspace. You may be prompted to log in if
   your workspace is not listed. If so, you may wish to log in using another
   tab - you will not be redirected back to this page:

.. figure:: /screenshots/Screenshot_20180411_232107.png

3. Under "Add features and functionality", click "Permissions":

.. figure:: /screenshots/Screenshot_20180416_170851.png

4. Add the following permission scopes, then "Save Changes":
    * users:read
    * channels:history
    * groups:history
    * im:history
    * mpim:history
    * channels:read
    * groups:read
    * im:read
    * mpim:read

.. figure:: /screenshots/Screenshot_20180416_175300.png

5. Scroll back up and click "Install App to Workplace". When asked to confirm,
   click "Authorize":
.. figure:: /screenshots/Screenshot_20180416_183319.png

6. Your OAuth Access Token should now be visible under "Tokens for your
   Workspace". You're done!

