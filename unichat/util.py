import json
import logging.config
import os
import sys
import urllib.request
import yaml


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
    return json.loads(response_as_string)


class TokenStore(object):
    """
    Stores arbitrary data on a per-token basis.

    Right now it's just an extra layer of abstraction over a dict. It's here
    because there are places where a dict would suffice that I may need more
    permanent storage later and want to minimize changes.
    """

    def __init__(self):
        self._store = {}

    def has(self, token):
        return token in self._store

    def get(self, token):
        if not self.has_data(token):
            return None
        return self._store[token]

    def set(self, token, data):
        self._store[token] = data


def setup_logging():
    logging.basicConfig(format='[%(asctime)s.%(msecs)d] [%(levelname)-8s] [%(filename)-10s:%(lineno)d] %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S',
                        level=logging.DEBUG)
