.PHONY: install serve test

serve: 
	pipenv run gunicorn --reload unichat.app

install:
	pipenv install

test:
	@pipenv run ./sanity.py test.config > /dev/null # Errors are printed to stdout

test-verbose:
	pipenv run ./sanity.py test.config

