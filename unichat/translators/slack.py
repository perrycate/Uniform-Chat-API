"""
Translates incoming requests into proper queries against GroupMe's public API.
"""
import json

from unichat.errors import AuthenticationError, ServiceError
from unichat.models import User, Conversation, ConversationCollection, \
                                Message, MessageCollection
from unichat.util import make_request
from unichat.translators import Translator


class Slack(Translator):

    SERVICE = "Slack" # For identification in errors, etc.
    URL_BASE = 'https://slack.com/api'
    PAGING_DONE_TOKEN = 'done'

    def get_users(self, conversation_id, auth='', page=''):
        raise NotImplementedError

    def get_conversations_list(self, auth='', page=''):
        data = self._make_request('/conversations.list', auth)

        channels = []
        if 'channels' not in data:
            raise ServiceError
        for channel in data['channels']:
            channels.append(Conversation(cid=channel['id'],
                                         name=channel['name'],
                                         last_updated='')) # TODO workaround
        # TODO paging
        return ConversationCollection(channels, '')

    def get_conversation(self, conversation_id, auth='', page=''):
        data = self._make_request('/conversations.info', auth,
                                  {'channel': conversation_id})
        # TODO paging
        return Conversation(cid=data['channel']['id'],
                            name=data['channel']['name'],
                            # is last_read good enough for last_updated?
                            last_updated=data['channel']['last_read'])

    def get_messages(self, conversation_id, auth='', page=''):
        if page == Slack.PAGING_DONE_TOKEN:
            return MessageCollection([], next_page='')

        data = self._make_request('/conversations.history', auth,
                                  {'channel': conversation_id, 'cursor': page})

        messages = []
        if ('messages' not in data):
            raise ServiceError
        for message in data['messages']:
            messages.append(Message(mid='', # TODO standin: hash of data?
                                    uid=message['user'],
                                    user_name='', # TODO
                                    text=message['text'],
                                    time=message['ts'])) # TODO uniform format

        if 'has_more' in data and data['has_more']:
            if 'next_cursor' not in data['response_metadata']:
                raise ServiceError
            cursor = data['response_metadata']['next_cursor']
        else:
            cursor = Slack.PAGING_DONE_TOKEN

        return MessageCollection(messages, next_page=cursor)

    def _make_request(self, endpoint, auth, params={}):
        # Convenience method to reduce the number of arguments passed around

        data = make_request(Slack.URL_BASE, endpoint, auth, params, False)

        # Check for errors
        if data['ok'] != True:
            if 'error' in data:
                if data['error'] == 'not_authed':
                    raise AuthenticationError
                if data['error'] == 'missing_scope':
                    raise AuthenticationError
            raise ServiceError

        return data


