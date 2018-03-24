import json
import urllib.request
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


"""
Handles requests against GroupMe's public API.
"""
class GroupMeTranslator(Translator):

    url_base = 'https://api.groupme.com/v3'

    def get_users(self, conversation_id, auth='', page=''):
        # In groupme's API, members are embedded in the data for that specific
        # group
        group_data = make_request(GroupMeTranslator.url_base,
                                  '/groups/{}'.format(conversation_id),
                                  auth)
        members = []
        for m in group_data['members']:
            members.append(User(uid=m['id'], name=m['nickname']))

        result = {'data':members, 'status': '200'}
        return result


    def get_conversation(self, conversation_id, auth='', page=''):
        pass

    def get_messages(self, conversation_id, auth='', page=''):
        pass


# fetches resource at URL, converts JSON response to useful Object
def make_request(base_url, additional_url, token, params={}):
    # Note: This function may require modification to be more generally useful.
    # I am borrowing it from another project specifically designed to work with
    # groupme's API (but not others)

    url = base_url + additional_url + "?token=" + token
    for param, value in params.items():
        url += "&" + param + "=" + value

    response = urllib.request.urlopen(url)

    # Convert raw response to usable JSON object
    response_as_string = response.read().decode('utf-8')
    obj = json.loads(response_as_string)

    return obj["response"]

