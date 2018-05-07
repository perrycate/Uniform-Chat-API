.PHONY: install serve test

serve: 
	pipenv run gunicorn --reload --log-level=WARNING unichat.app

install:
	pipenv install

test:
	@pipenv run ./sanity_test.py test.config > /dev/null # Errors are printed to stdout

test-verbose:
	pipenv run ./sanity_test.py test.config

clean:
	rm *.log
