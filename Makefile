.PHONY: install serve test

serve: 
	pipenv run gunicorn --reload unichat.app

install:
	pipenv install

# Just check for an HTTP error on a request for now
test:
	./sanity-test.sh

