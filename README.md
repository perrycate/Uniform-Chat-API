# Uniform Chat API
## Terminology
 * **Handler** : Handles all incoming HTTP requests for a particular resource,
    invoking the appropriate translator, and eventually returning the result in
    a uniform format.
 * **Translator**: Makes outgoing requests to a particular service.

## Testing

Note: Currently `make test` only runs a very basic test to see if the server
returns an HTTP error for a valid request, with no other checks of any kind.

Prerequisites: User must have Python 3, pip, and pipenv installed

In one terminal:

    $ make install # (If this is the first time)
    $ make serve

In another:

    $ make test

Or, for more verbose output (like the JSON returned from each request):

    $ make test-verbose

