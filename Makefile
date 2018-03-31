.PHONY: install serve test

serve: 
	pipenv run gunicorn --reload unichat.app

install:
	pipenv install

test:
	@./sanity.py > /dev/null # Errors are printed to stdout

test-verbose:
	./sanity.py

