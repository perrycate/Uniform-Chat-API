"""
Translates incoming requests into proper queries against GroupMe's public API.
"""
from unichat.models import User, Conversation, ConversationCollection, \
                                Message, MessageCollection
from unichat.util import make_request
from unichat.translators import Translator


class Slack(Translator):

    url_base = ''
    def get_users(self, conversation_id, auth='', page=''):
        raise NotImplementedError

    def get_conversations_list(self, auth='', page=''):
        raise NotImplementedError

    def get_conversation(self, conversation_id, auth='', page=''):
        raise NotImplementedError

    def get_messages(self, conversation_id, auth='', page=''):
        raise NotImplementedError

