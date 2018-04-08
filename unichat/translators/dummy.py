"""
Mock handler just to test that the rest of the code works elsewhere
"""
# A cleaner approach would be to define our own set of errors and have them map
# to falcon HTTP errors
from falcon import HTTP_200

from unichat.models import User, Conversation, ConversationCollection, \
                                Message, MessageCollection
from unichat.translators import Translator

class Dummy(Translator):

    def get_conversations_list(self, auth='', page=''):
        return ConversationCollection(
                [
                    Conversation(cid='4d7123',
                                 name='IW Chat Group',
                                 last_updated=123456789),
                    Conversation(cid='9d2asdf',
                                 name='Some other Group',
                                 last_updated=123456799),
                ],
                next_page='somepagetoken4321')

    def get_users(self, conversation_id, auth='', page=''):
        return [User(uid=12345,name="Perry"), User(uid=32123,name="Jérémie")]

    def get_conversation(self, conversation_id, auth='', page=''):
        return Conversation(
                cid=conversation_id,
                name='IW Chat Group',
                last_updated=123456788)

    def get_messages(self, conversation_id, auth='', page=''):
        return MessageCollection(
                messages=[
                    Message(
                        mid=5789,
                        uid=12345,
                        user_name='Perry',
                        text='Hello, World!',
                        time=1521030283),
                    Message(
                        mid=6790,
                        uid=32123,
                        user_name='Jérémie',
                        text='Good to see you!',
                        time=1521030283),
                ],
                next_page='somepagetoken1234'
            )
