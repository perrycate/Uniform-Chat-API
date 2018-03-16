# Uniform Chat API
## Terminology
 * **Handler** : Handles all incoming HTTP requests for a particular resource,
    invoking the appropriate translator, and eventually returning the result in
    a uniform format.
 * **Translator**: Makes outgoing requests to a particular service.

## Testing

In one terminal:

    $ pipenv install # (If this is the first time)
    $ pipenv shell
    $ gunicorn --reload unichat.app


In another:

    $ pipenv shell
    $ http localhost:8000/dummy/conversations/42?token=AUTH

