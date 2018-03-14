In one terminal:

    $ pipenv install # (If this is the first time)
    $ pipenv shell
    $ gunicorn --reload unichat.app


In another:

    $ pipenv shell
    $ http localhost:8000/dummy/conversations/42?token=AUTH

