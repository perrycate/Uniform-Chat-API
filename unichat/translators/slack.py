"""
Translates incoming requests into proper queries against GroupMe's public API.
"""
import json

from unichat.errors import AuthenticationError, ServiceError, UnauthorizedError
from unichat.models import User, Conversation, ConversationCollection, \
                                Message, MessageCollection
from unichat.util import make_request, TokenStore
from unichat.translators import Translator


class Slack(Translator):

    SERVICE = 'Slack' # For identification in errors, etc.
    URL_BASE = 'https://slack.com/api'
    PAGING_DONE_TOKEN = 'done'

    def __init__(self):
        self._token_store = TokenStore()

    def get_users(self, conversation_id, auth=''):
        # Get list of users in this chat (this only gives us IDs though)
        user_ids = []
        page = ''
        pages_remain = True
        while pages_remain:
            users_list_raw = self._make_request('/conversations.members', auth,
                                                {'channel': conversation_id,
                                                 'cursor': page})
            # Add users retrieved
            if 'members' not in users_list_raw:
                raise ServiceError
            user_ids += users_list_raw['members']

            # Keep going as long as there are more users to retrieve
            pages_remain = self._has_pages_remaining(users_list_raw)
            if pages_remain:
                page = self._get_page_cursor(users_list_raw)

        # Associate names etc with user ids
        all_users = self._fetch_users_info(auth)
        users_in_chat = []
        for uid in user_ids:
            if uid not in all_users:
                raise ServiceError
            users_in_chat.append(all_users[uid])

        return users_in_chat

    def get_conversations_list(self, auth='', page=''):
        # Retrieve conversations data, populate list
        if page == Slack.PAGING_DONE_TOKEN:
            return ConversationCollection([], '')

        channels = []
        pages_remain = True
        while pages_remain:
            data = self._make_request('/conversations.list', auth,
                                      {'cursor': page})
            # Add conversations retrieved
            if 'channels' not in data:
                raise ServiceError
            for channel in data['channels']:
                channels.append(Conversation(cid=channel['id'],
                                             name=channel['name'],
                                             last_updated='')) # TODO workaround
            pages_remain = self._has_pages_remaining(data)
            if pages_remain:
                page = sef._get_page_cursor(data)
            else:
                page = Slack.PAGING_DONE_TOKEN

        return ConversationCollection(channels, page)

    def get_conversation(self, conversation_id, auth=''):
        data = self._make_request('/conversations.info', auth,
                                  {'channel': conversation_id})

        return Conversation(cid=data['channel']['id'],
                            name=data['channel']['name'],
                            # is last_read good enough for last_updated?
                            last_updated=data['channel']['last_read'])

    def get_messages(self, conversation_id, auth='', page=''):
        if page == Slack.PAGING_DONE_TOKEN:
            return MessageCollection([], next_page='')

        # Retrieve message data
        data = self._make_request('/conversations.history', auth,
                                  {'channel': conversation_id, 'cursor': page})
        if ('messages' not in data):
            raise ServiceError

        # populate array of message objects
        messages = []
        users = self._fetch_users_info(auth)
        for index in range(len(data['messages'])):
            message = data['messages'][index]

            # Unsupported event
            # FIXME: some important events are not captured this way
            # (e.g., message_changed, message_replied)
            # https://api.slack.com/events/message
            if not 'user' in message:
                continue

            message_id = self._create_message_id(conversation_id, page, index)
            user_id = message['user']
            user = users[user_id]
            messages.append(Message(mid=message_id,
                                    uid=user_id,
                                    user_name=user.name,
                                    text=message['text'],
                                    time=message['ts'])) # TODO uniform format

        # Check for pagination token
        if 'has_more' in data and data['has_more']:
            if 'next_cursor' not in data['response_metadata']:
                raise ServiceError
            cursor = data['response_metadata']['next_cursor']
        else:
            cursor = Slack.PAGING_DONE_TOKEN

        return MessageCollection(messages, next_page=cursor)

    def _make_request(self, endpoint, auth, params={}):
        # Convenience method to reduce the number of arguments passed around
        data = make_request(Slack.URL_BASE, endpoint, auth, params)

        # Check for errors
        if data['ok'] != True:
            if 'error' in data:
                if (data['error'] == 'not_authed') or (data['error'] == 'invalid_auth'):
                    raise AuthenticationError
                if data['error'] == 'missing_scope':
                    raise UnauthorizedError
                raise ServiceError(data['error'])
            raise ServiceError(data)

        return data

    def _fetch_users_info(self, token):
        # Get users in the slack associated with this token, if we haven't yet.

        # Check for cached result
        if self._token_store.has_data(token):
            return self._token_store.get_data(token)

        # request users list, iterating over pages
        pages_remaining = True
        page = ''
        users = {}
        while pages_remaining:
            data = self._make_request('/users.list', token,
                                      {'limit': 1000, 'cursor': page})
            if 'members' not in data:
                raise ServiceError
            for user_raw in data['members']:
                uid = user_raw['id']
                users[uid] = User(uid=uid, name=user_raw['name'])

            # Handle paging
            if self._has_pages_remaining(data):
                page = data['response_metadata']['next_cursor']
            else:
                pages_remaining = False

        # Cache users for next time
        self._token_store.set_data(token, users)

        # It's cached now and I don't want to repeat myself
        return self._fetch_users_info(token)

    def _has_pages_remaining(self, data):
        return 'response_metadata' in data and \
               'next_cursor' in data['response_metadata'] and \
               data['response_metadata']['next_cursor'] is not ''

    def _get_page_cursor(self, data):
        return data['response_metadata']['next_cursor']

    def _create_message_id(self, cid, cursor, index):
        return '{}@{}@{}'.format(cid, cursor, index)

