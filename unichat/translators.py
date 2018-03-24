from abc import ABC, abstractmethod

# A cleaner approach would be to define our own set of errors and have them map
# to falcon HTTP errors, but I'm not convinced that that would be worth it here.
from falcon import HTTP_200

from unichat.models import User, Conversation, Message, MessageCollection

"""
Handles outgoing requests to a particular service. Accepts given parameters,
makes whatever request(s) is necessary to the corresponding service, and returns
data in a uniform format.
"""
class Translator(ABC):

    @abstractmethod
    def get_users(self, conversation_id, auth, page):
        pass

    @abstractmethod
    def get_conversation(self, conversation_id, auth, page):
        pass

    @abstractmethod
    def get_messages(self, conversation_id, auth, page):
        pass


"""
Mock handler just to test that the rest of the code works elsewhere
"""
class DummyTranslator(Translator):


    def get_users(self, conversation_id, auth='', page=''):
        result = {'data': {}, 'status': HTTP_200}

        result['data'] = [User(uid=12345,name="Perry"),
                          User(uid=32123,name="Jérémie")]

        return result


    def get_conversation(self, conversation_id, auth='', page=''):
        result = {'data': {}, 'status': HTTP_200}

        result['data'] = Conversation(
                cid=conversation_id,
                name='IW Chat Group',
                messages=[
                    Message(
                        mid=5789,
                        uid=12345,
                        user_name='Perry',
                        text='Hello, World!',
                        time=1521030283
                    ),
                    Message(
                        mid=6790,
                        uid=32123,
                        user_name='Jérémie',
                        text='Good to see you!',
                        time=1521030283,
                    )
                ],
                next_page='somepagetoken1234'
            )

        return result


    def get_messages(self, conversation_id, auth='', page=''):
        result = {'data': {}, 'status': HTTP_200}

        result['data'] = MessageCollection(
                messages=[
                    Message(
                        mid=5789,
                        uid=12345,
                        user_name='Perry',
                        text='Hello, World!',
                        time=1521030283
                    ),
                    Message(
                        mid=6790,
                        uid=32123,
                        user_name='Jérémie',
                        text='Good to see you!',
                        time=1521030283,
                    )
                ],
                next_page='somepagetoken1234'
            )

        return result
