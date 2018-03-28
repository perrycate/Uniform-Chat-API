import json
import urllib.request
from abc import ABC, abstractmethod

# A cleaner approach would be to define our own set of errors and have them map
# to falcon HTTP errors
from falcon import HTTP_200

from unichat.models import User, Conversation, ConversationCollection, \
                                Message, MessageCollection

"""
Handles outgoing requests to a particular service. Accepts given parameters,
makes whatever request(s) is necessary to the corresponding service, and returns
data in a uniform format.
"""
class Translator(ABC):

    @abstractmethod
    def get_conversations_list(self, auth, page):
        pass

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
class Dummy(Translator):


    def get_conversations_list(self, auth='', page=''):
        result = {'data': {}, 'status': HTTP_200}

        result['data'] = ConversationCollection(
                [Conversation(cid='4d7123', name='IW Chat Group'),
                 Conversation(cid='9d2asdf', name='Some other Group')],
                next_page='somepagetoken4321')

        return result


    def get_users(self, conversation_id, auth='', page=''):
        result = {'data': {}, 'status': HTTP_200}

        result['data'] = [User(uid=12345,name="Perry"),
                          User(uid=32123,name="Jérémie")]

        return result


    def get_conversation(self, conversation_id, auth='', page=''):
        result = {'data': {}, 'status': HTTP_200}

        result['data'] = Conversation(
                cid=conversation_id,
                name='IW Chat Group'
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
Translates incoming requests into proper queries against GroupMe's public API.
"""
class GroupMe(Translator):

    url_base = 'https://api.groupme.com/v3'
    DM_ID_PREFIX = 'D'
    GROUP_ID_PREFIX = 'G'
    assert len(DM_ID_PREFIX) == len(GROUP_ID_PREFIX)
    ID_PREFIX_LENGTH = len(DM_ID_PREFIX)

    def get_users(self, conversation_id, auth='', page=''):

        members = []
        if self._is_direct_message(conversation_id):
            # Expected conversation id: D + other user ID
            cid = self._convo_to_groupme_id(conversation_id)

            # Add other user
            dm_data = make_request(GroupMe.url_base,
                                   '/direct_messages/{}'.format(cid), auth)
            members.append(User(uid=dm_data['direct_messages']['user_id'],
                            name=dm_data['direct_messages']['name']))

            # Add ourselves
            self_data = make_request(GroupMe.url_base, '/users/me', auth)
            members.append(User(uid=self_data['id'], name=self_data['name']))
        else:
            # Expected conversation id: G + group ID
            gid = self._convo_to_groupme_id(conversation_id)
            data = make_request(GroupMe.url_base,
                                '/groups/{}'.format(gid), auth)
            for m in data['members']:
                members.append(User(uid=m['id'], name=m['nickname']))

        return {'data':members, 'status': '200'} # TODO error handling

    def get_conversations_list(self, auth='', page=''):
        # Reminder: change DM conversation ID to [G|D] + other user ID

        # TODO hit /chats (possibly multiple times?), mix with groups, sort,
        # return top 100? idk but make sure it's pageable

        # IDEA: in page token: indexes (page and offset) into both groups and DMs 

        pass

    def get_conversation(self, conversation_id, auth='', page=''):
        result = {'data': {}, 'status': HTTP_200} # TODO error handling

        if self._is_direct_message(conversation_id):
            # Expected conversation id: D + other user ID
            other_user_id = self._convo_to_groupme_id(conversation_id)

            # Add other user
            dm_data = make_request(GroupMe.url_base, '/direct_messages',
                                   auth, {'other_user_id': other_user_id})

            # False only if there's a code error, _not_ user error
            assert other_user_id == dm_data['direct_messages']['recipient_id']

            result['data'] = Conversation(
                    cid=self._dm_to_convo_id(other_user_id),
                    name=dm_data['direct_messages']['name'])
        else:
            gid = self._convo_to_groupme_id(conversation_id)
            group_data = make_request(GroupMe.url_base,
                                      '/groups/{}'.format(gid), auth)
            result['data'] = Conversation(
                    cid=group_data['id'],
                    name=group_data['name'])

        return result

    def get_messages(self, conversation_id, auth='', page=''):
        pass

    def _is_direct_message(cls, conversation_id: str) -> bool:
        return conversation_id.startswith(cls.DM_ID_PREFIX)

    def _convo_to_groupme_id(cls, conversation_id: str) -> str:
        # Convert client-facing conversation_id into the format groupme expects
        return conversation_id[cls.ID_PREFIX_LENGTH:]

    def _dm_to_convo_id(cls, other_user_id: str) -> str:
        # NOTE: Because of how groupme retrieves direct messages, we use the
        # ID of the other user, not the 'id' property of direct messages
        return cls.DM_ID_PREFIX + other_user_id


# fetches resource at URL, converts JSON response to useful Object
def make_request(base_url, additional_url, token, params={}):
    # Note: This function may require modification to be more generally useful.
    # I am borrowing it from another project specifically designed to work with
    # groupme's API

    url = base_url + additional_url + "?token=" + token
    for param, value in params.items():
        url += "&" + param + "=" + value

    response = urllib.request.urlopen(url)

    # Convert raw response to usable JSON object
    response_as_string = response.read().decode('utf-8')
    obj = json.loads(response_as_string)

    return obj["response"]

