#!/usr/bin/env python3
"""
An assortment of tests for each service to make sure the API isn't broken.

For each service, hit every endpoint and make sure it returns the
proper HTTP status code. Does not check content of response other
than status code.
"""
import json
import sys
import urllib.request

from unichat.translators import GroupMe
from unichat.util import print_err

def main():
    has_config = len(sys.argv) > 1
    if has_config:
        config = open(sys.argv[1])
    else:
        print_err('WARNING: No config file provided. Tests requiring '
                  'authentication may fail.')
        token = ''

    summary = []
    for test in [test_dummy,test_groupme]:
        if has_config:
            token = config.readline().strip()
        service, oks, fails, errors = test(token)
        summary.append('{:<12} {} OK, {} FAIL, {} ERRORS'.format(
                service + ':', oks, fails, errors))

    for s in summary:
        print_err(s)


def test_dummy(token):
    endpoints = [
        'http://localhost:8000/dummy/conversations',
        'http://localhost:8000/dummy/conversations/42',
        'http://localhost:8000/dummy/conversations/42/users',
        'http://localhost:8000/dummy/conversations/42/messages'
    ]
    oks, fails, errors = 0, 0, 0

    for url in endpoints:
        oks, fails, errors, _ = test_url(url, oks, fails, errors)
    return ('dummy', oks, fails, errors)


def test_groupme(token):

    primary_endpoint = 'http://localhost:8000/groupme/conversations?token={}'
    endpoints = [
        'http://localhost:8000/groupme/conversations/{}?token={}',
        'http://localhost:8000/groupme/conversations/{}/users?token={}',
        'http://localhost:8000/groupme/conversations/{}/messages?token={}'
    ]
    oks, fails, errors = 0, 0, 0

    oks, fails, errors, data = test_url(primary_endpoint.format(token),
                                          oks, fails, errors)
    if data is None or 'conversations' not in data:
        # Whelp, can't do anything else.
        return ('groupme', oks, fails, errors)
    data = json.loads(data)

    # Because the underlying groupme implementation behaves differently between
    # direct messages (dms) and group chats, (groups), we test endpoints twice,
    # for both types of conversations.
    # It's unlikely the user has no DMs or no groups. This is just a test
    # script, so I'm not going to bother checking that edge case..
    conversations = data['conversations']
    chat = conversations[0]['id']

    # This is cheating, but necessary
    first_dm_status = GroupMe._is_direct_message(chat)

    for url in endpoints:
        url = url.format(chat, token)
        oks, fails, errors, _ = test_url(url, oks, fails, errors)

    for chat in data['conversations']:
        # If the first was a group, find a dm. If it was a dm, find a group.
        chat = chat['id']
        if GroupMe._is_direct_message(chat) == first_dm_status:
            continue

        # Rerun tests on other conversation type
        for url in endpoints:
            url = url.format(chat, token)
            oks, fails, errors, _ = test_url(url, oks, fails, errors)
        break


    return ('groupme', oks, fails, errors)


def test_url(url, oks, fails, errs):
    print(url)
    try:
        response = urllib.request.urlopen(url)
        data = json.dumps(json.loads(response.read().decode('utf-8')),
                          indent=4)
        print(data)
        print()
        if response.getcode() != 200:
            fails += 1
        else:
            oks += 1

        return oks, fails, errs, data
    except urllib.request.HTTPError as e:
        print_err('{} returned by {}'.format(e, url))
        fails += 1
    except Exception as e:
        print_err('{} - {}'.format(e, url))
        errs += 1
    return oks, fails, errs, None


main()
