#!/usr/bin/env python3
"""
An assortment of tests for each service to make sure the API isn't broken.

For each service, hit every endpoint and make sure it returns the
proper HTTP status code. Does not check content of response other
than status code.
"""
import json
import urllib.request

from unichat.util import print_err

def main():
    summary = []
    for test in [test_dummy,]:
        service, oks, fails, errors = test()

        summary.append('{:<12} {} OK, {} FAIL, {} ERRORS'.format(
                service + ':', oks, fails, errors))

    for s in summary:
        print_err(s)

def test_dummy():
    endpoints = [
        'http://localhost:8000/dummy/conversations',
        'http://localhost:8000/dummy/conversations/42',
        'http://localhost:8000/dummy/conversations/42/users',
        'http://localhost:8000/dummy/conversations/42/messages'
    ]
    oks = 0
    fails = 0
    errors = 0

    for url in endpoints:
        print(url)
        try:
            response = urllib.request.urlopen(url)
            print(json.dumps(json.loads(response.read().decode('utf-8')),
                             indent=4))
            print()
            if response.getcode() != 200:
                fails += 1
            else:
                oks += 1
        except urllib.request.HTTPError as e:
            print_err('{} returned by {}'.format(e, url))
            fails += 1
        except Exception as e:
            print_err('{} - {}'.format(e, url))
            errors += 1
            continue
    return ('dummy', oks, fails, errors)

main()
