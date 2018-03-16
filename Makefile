.PHONY: install serve test

serve: 
	pipenv run gunicorn --reload unichat.app

install:
	pipenv install

# Just check for an HTTP error on a request for now
test:
	@pipenv run http localhost:8000/dummy/conversations/42?token=AUTH\
		--check-status; if [ $$? -ne 0 ] ; then echo "Sanity check FAILED!" ;\
		else echo "Sanity check passed :)" ; fi
