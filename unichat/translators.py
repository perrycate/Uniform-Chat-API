from abc import ABC, abstractmethod

# A cleaner approach would be to define our own set of errors and have them map
# to falcon HTTP errors, but I'm not convinced that that would be worth it here.
from falcon import HTTP_200

"""
Handles outgoing requests to a particular service. Accepts given parameters,
makes whatever request(s) is necessary to the corresponding service, and returns
data in a uniform format.
"""
class Translator(ABC):
    @abstractmethod
    def get_conversation(self, conversation_id, auth, page):
        pass

"""
Mock handler just to test that the rest of the code works elsewhere
"""
class DummyTranslator(Translator):


    def get_users(self, conversation_id, auth='', page=''):
        result = {'data': {}, 'status': HTTP_200}

        # The Java Programmer in me would like to see a result datatype to
        # enforce the data is passed around in a consistent format. Does that
        # seem reasonable?
        result['data'] = [
            {
            'id': 12345,
            'name': 'IW Chat Group'
            },
            {
            'id': 32123,
            'name': 'IW Chat Group'
            }
        ]

        return result


    def get_conversation(self, conversation_id, auth='', page=''):
        result = {'data': {}, 'status': HTTP_200}

        # The Java Programmer in me would like to see a result datatype to
        # enforce the data is passed around in a consistent format. Does that
        # seem reasonable?
        result['data'] = {
            'id': conversation_id,
            'name': 'IW Chat Group',
            'messages': [
                {
                    'msgId': 6789,
                    'userId': 12345,
                    'userName': 'Perry',
                    'text': 'Hello, World!',
                    'attachments': [],
                    'time': 1521030283,
                },
                {
                    'msgId': 6790,
                    'userId': 32123,
                    'userName': 'Jérémie',
                    'text': 'Good to see you!',
                    'attachments': [],
                    'time': 1521030294,
                },
            ],
            'next_page': 'somepagetoken1234'
        }

        return result


    def get_messages(self, conversation_id, auth='', page=''):
        result = {'data': {}, 'status': HTTP_200}

        # The Java Programmer in me would like to see a result datatype to
        # enforce the data is passed around in a consistent format. Does that
        # seem reasonable?
        result['data'] = {
            'messages': [
                {
                    'msgId': 6789,
                    'userId': 12345,
                    'userName': 'Perry',
                    'text': 'Hello, World!',
                    'attachments': [],
                    'time': 1521030283,
                },
                {
                    'msgId': 6790,
                    'userId': 32123,
                    'userName': 'Jérémie',
                    'text': 'Good to see you!',
                    'attachments': [],
                    'time': 1521030294,
                },
            ],
            'next_page': 'somepagetoken1234'
        }

        return result