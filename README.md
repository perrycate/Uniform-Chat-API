# Uniform Chat API
## Acquiring Access Tokens
### GroupMe Instructions
1. Log into `dev.groupme.com`:
![Screenshot of dev.groupme.com with login circled](/docs/screenshots/Screenshot_20180411_224924.png)

2. Click "Access Token" in the upper right corner:
![Screenshot of dev.groupme.com, logged in, with "Access Token" circled](/docs/screenshots/Screenshot_20180411_225501.png)

3. You should see a popup with your API Access token. You're done!

### Slack Instructions
1. Go to `api.slack.com` and click "Start Building":
![Screenshot of api.slack.com with "Start Building" circled](/docs/screenshots/Screenshot_20180411_231758.png)

2. Enter an app name and select a workspace. You may be prompted to log in if your workspace is not listed:
![Screenshot of the dialog for creating a slack app](/docs/screenshots/Screenshot_20180411_232107.png)

3. Under "Add features and functionality", click "Permissions":
![Screenshot of the dialog for creating a slack app](/docs/screenshots/Screenshot_20180416_170851.png)

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
![Screenshot of the section of the page for adding scopes](/docs/screenshots/Screenshot_20180416_175300.png)

5. Scroll back up and click "Install App to Workplace". When asked to confirm, click "Authorize":
![Screenshot of the section of the page with the install button circled](/docs/screenshots/Screenshot_20180416_183319.png)

6. Your OAuth Access Token should now be visible under "Tokens for your Workspace". You're done!

## Contributing
### Terminology
 * **Handler** : Handles all incoming HTTP requests for a particular resource,
    invoking the appropriate translator, and eventually returning the result in
    a uniform format.
 * **Translator**: Makes outgoing requests to a particular service.
 * **Service**: Any messaging API we can make outgoing queries against.

### Relevant files
 * `sanity.py`: Basic tests to make sure the API isn't completely broken.
 * `unichat/app.py`: Sets everything up. Configures handlers+endpoints, routes,
        errors, etc.
 * `unichat/errors.py`: Maps raisable exceptions to error handling code.
 * `unichat/models.py`: Defines basic data objects passed between handlers and
        translators.
 * `unichat/util.py`: Contains various generically useful helper functions.
 * `unichat/handlers.py`: Defines falcon Resources for each endpoint. Handlers
        invoke the appropriate translator depending on the service requested.
 * `unichat/translators/*`: Contains Translators to manage requests to various
        messaging APIs.

### Testing
Note: Currently `make test` only runs a very basic test to see if the server
returns an HTTP error for a valid request, with no other checks of any kind.

Prerequisites: User must have Python 3, pip, and pipenv installed
Before running tests, modify test.config.sample (adding authentication tokens
as necessary) and save it as test.congig. Otherwise, any tests requiring
authentication will fail.

In one terminal:

    $ make install # (If this is the first time)
    $ make serve

In another:

    $ make test

Or, for more verbose output (such as the JSON returned from each request):

    $ make test-verbose

### Documentation
To generate and view the documentation: (after running `make install` in the
base directory):

    cd ./docs
    make livehtml

This will run an auto-reloading server on port 8000. 
