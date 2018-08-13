"""
Translates incoming requests into proper queries against GroupMe's public API.
"""
import json
import logging
import fbchat

from unichat.errors import AuthenticationError, ServiceError, NotFoundError, \
                                UnauthorizedError
from unichat.models import User, Conversation, ConversationCollection, \
                                Message, MessageCollection
from unichat.util import make_request, TokenStore
from unichat.translators import Translator


class Facebook(Translator):

    SERVICE = 'Facebook' # For identification in errors, etc.
    PAGING_DONE_TOKEN = 'done'

    def __init__(self):
        # Contains fb client instances for each user
        self._clients = TokenStore()

    def get_users(self, conversation_id, auth=''):
        # TODO
        user_ids = None # TODO

        # Associate names etc with user ids
        all_users = self._fetch_users_info(auth)
        users_in_chat = []
        for uid in user_ids:
            if uid not in all_users:
                raise ServiceError('Unknown UID {}'.format(uid))
            users_in_chat.append(all_users[uid])

        return users_in_chat

    # TODO verify works
    def get_conversations_list(self, auth='', page=''):
        client = self._get_client(auth)

        # TODO unify date format
        convos = map(lambda t: Conversation(t.uid, t.name,
                                            t.last_message_timestamp),
                     client.fetchThreadList())

        return ConversationCollection(convos, '')  # TODO paging

    def get_conversation(self, conversation_id, auth=''):
        # TODO

        return Conversation(cid=data['channel']['id'],
                            name=data['channel']['name'],
                            # is last_read good enough for last_updated?
                            last_updated=data['channel']['last_read'])

    def get_messages(self, conversation_id, auth='', page=''):
        pass
        # TODO

    def _get_client(self, auth):
        """
        Returns fb client oject for the user associated with this token.

        auth must be a string of the format fb_username:fb_password
        """

        # Check if cached copy exists
        cached = self._client_store.get(auth)
        if cached is not None:
            return cached

        # Get creds from auth token 
        split = auth.partition(':')
        if split[1] != ':':
            # auth didn't contain a ':', format was unexpected
            raise ValueError("Invalid Facebook auth token: {}".format(auth))
        username = split[0]
        password = split[2]

        client = fbchat.Client(username, password)
        self._clients.set(auth, client)
        return client


    def _fetch_users_info(self, token):
        """Get users in fb associated with this token"""
        # TODO

        # Check for cached result
        if self._token_store.has(token):
            return self._token_store.get(token)

        # request users list, iterating over pages
        pages_remaining = True
        page = ''
        users = {}
        while pages_remaining:
            data = self._make_request('/users.list', token,
                                      {'limit': 1000, 'cursor': page})
            if 'members' not in data:
                raise ServiceError('Missing \'members\' field:'
                                   '{}'.format(data))
            for user_raw in data['members']:
                uid = user_raw['id']
                users[uid] = User(uid=uid, name=user_raw['name'])

            # Handle paging
            if self._has_pages_remaining(data):
                page = data['response_metadata']['next_cursor']
            else:
                pages_remaining = False

        # Cache users for next time
        self._token_store.set(token, users)

        # It's cached now and I don't want to repeat myself
        return self._fetch_users_info(token)

    def _has_pages_remaining(self, data):
        # TODO even necessary?
        return 'response_metadata' in data and \
               'next_cursor' in data['response_metadata'] and \
               data['response_metadata']['next_cursor'] is not ''

    def _get_page_cursor(self, data):
        # TODO even necessary?
        return data['response_metadata']['next_cursor']

