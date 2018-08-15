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
        self._users = TokenStore()

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

        return ConversationCollection(list(convos), '')  # TODO paging

    # TODO verify works
    def get_conversation(self, conversation_id, auth=''):
        client = self._get_client(auth)
        thread = client.fetchThreadInfo(conversation_id)

        # TODO unify date format
        return Conversation(cid=thread.uid,
                            name=thread.name,
                            # is last_read good enough for last_updated?
                            last_updated=thread.last_message_timestamp)

    # TODO verify works
    def get_messages(self, conversation_id, auth='', page=''):
        client = self._get_client(auth)
        users = self._fetch_users_info(auth)
        fbchat_message_list = client.fetchThreadMessages(conversation_id)

        messages = map(lambda m: Message(mid=m.uid,
                                         uid=m.author,
                                         user_name=users[m.author].name,
                                         text=m.text,
                                         time=m.timestamp),
                       fbchat_message_list)
        return MessageCollection(list(messages), '')  # TODO paging

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

        try:
            client = fbchat.Client(username, password)
        except FBChatUserError as e:
            raise AuthenticationError(e)

        self._clients.set(auth, client)
        return client


    def _fetch_users_info(self, token):
        """Get users in fb associated with this token"""

        # Check for cached result
        if self._tokens.has(token):
            return self._tokens.get(token)

        # request users list, iterating over pages
        client = self._get_client(token)
        fbchat_users = client.fetchAllUsers()
        users_dict = {}
        for user in fbchat_users:  # TODO this can definitely be a 1-liner
            users_dict[user.uid] = user

        # Cache users for next time
        self._tokens.set(token, users_dict)

        return users_dict

    def _has_pages_remaining(self, data):
        # TODO even necessary?
        return 'response_metadata' in data and \
               'next_cursor' in data['response_metadata'] and \
               data['response_metadata']['next_cursor'] is not ''

    def _get_page_cursor(self, data):
        # TODO even necessary?
        return data['response_metadata']['next_cursor']

