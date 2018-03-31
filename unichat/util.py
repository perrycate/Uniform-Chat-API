import json
import sys
import urllib.request


def print_err(*args, **kwargs):
    """Behaves exactly like print(), but to stderr."""
    print(*args, file=sys.stderr, **kwargs)


def make_request(base_url, additional_url, token, params={}):
    """Fetches resource at URL, converts JSON response to object."""

    # Note: This function may require modification to be more generally useful.
    # I am borrowing it from another project specifically designed to work with
    # groupme's API

    url = base_url + additional_url + "?token=" + token
    for param, value in params.items():
        url += "&" + param + "=" + str(value)

    response = urllib.request.urlopen(url)

    # Convert raw response to usable JSON object
    response_as_string = response.read().decode('utf-8')
    obj = json.loads(response_as_string)

    return obj["response"]

