from abc import ABC, abstractmethod

# A cleaner approach would be to define our own set of errors and have them map
# to falcon HTTP errors, but I'm not convinced that that would be worth it here.
from falcon import HTTP_200


class Handler(ABC):
    @abstractmethod
    def handle_request(self, conversation_id, auth, page):
        pass

"""
Mock handler just to test that the rest of the code works elsewhere
"""
class DummyHandler(Handler):

    def handle_request(self, conversation_id, auth='', page=''):
        result = {'data': {}, 'status': HTTP_200}

        # The Java Programmer in me would like to see a result datatype to
        # enforce the data is passed around in a consistent format. Does this
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