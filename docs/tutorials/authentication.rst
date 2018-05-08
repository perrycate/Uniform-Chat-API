.. _authentication:

Authentication
==============================

.. NOTE. I would have some introduction, such as explaining what are these
   tokens, that they are personal to the developer, and should not be
   distributed. If Unichat is deployed as part of some other service, then
   care must be taken to retrieve the user's token (not the developer's).
   In fact, it is one future feature of Unichat to be able to retrieve the
   tokens through some OAuth type UI request.

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
   your workspace is not listed:

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

6. Your OAuth Access Token should now be visible under "Tokens for your Workspace". You're done!

