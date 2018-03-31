import json
import urllib.request
from abc import ABC, abstractmethod

# A cleaner approach would be to define our own set of errors and have them map
# to falcon HTTP errors
from falcon import HTTP_200

from unichat.models import User, Conversation, ConversationCollection, \
                                Message, MessageCollection
from unichat.util import make_request

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
                [Conversation(cid='4d7123', name='IW Chat Group',
                              last_updated=123456789),
                 Conversation(cid='9d2asdf', name='Some other Group',
                              last_updated=123456799)],
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
                name='IW Chat Group',
                last_updated=123456788
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
    DMS_PER_PAGE = 100
    GROUPS_PER_PAGE = 100
    DM_ID_PREFIX = 'D'
    GROUP_ID_PREFIX = 'G'
    assert len(DM_ID_PREFIX) == len(GROUP_ID_PREFIX)
    ID_PREFIX_LENGTH = len(DM_ID_PREFIX)

    def get_users(self, conversation_id, auth='', page=''):

        members = []
        if GroupMe._is_direct_message(conversation_id):
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

    def get_conversations_list(self, auth='', page='1:0-1:0'):

        # Page token format: '(DM Page):(DM Index)-(Groups Page):(Groups index)
        dms, groups = page.split('-')
        dms_page, dms_offset = [int(x) for x in dms.split(':')]
        groups_page, groups_offset = [int(x) for x in groups.split(':')]

        # Retrieve direct messages, convert to Conversations
        dms = []
        dms_raw = make_request(
            GroupMe.url_base, '/chats', auth,
            {'page': dms_page, 'per_page': GroupMe.DMS_PER_PAGE}
        )
        i = 0
        # Skip to offset
        dms_raw = dms_raw[dms_offset:]
        for dm in dms_raw:
            dm_object = Conversation(
                    cid=self._dm_to_convo_id(dm['other_user']['id']),
                    name=dm['other_user']['name'],
                    last_updated=float(dm['updated_at']))
            dm_object.index = i # Ad-hoc property, determines new index later
            dms.append(dm_object)
            i += 1

        # Retrieve group messages, convert to Conversations
        groups = []
        groups_raw = make_request(
            GroupMe.url_base, '/groups', auth,
            {'page': groups_page, 'per_page': GroupMe.GROUPS_PER_PAGE}
        )
        i = 0
        for group in groups_raw:
            group_object = Conversation(
                cid=self._group_to_convo_id(group['id']),
                name=group['name'],
                last_updated=float(group['updated_at']))
            group_object.index = i # Ad-hoc property, determins new index later
            groups.append(group_object)
            i += 1

        # Combine chats and groups, sort by updated_at
        combined = sorted((dms + groups), key=lambda c: c.last_updated,
                          reverse=True)

        # Find new offsets
        num_groups, num_dms = len(groups), len(dms)
        groups_count, dms_count = 0, 0
        for conversation in combined:
            if GroupMe._is_direct_message(conversation.cid):
                dms_count += 1
                if dms_count == num_dms and num_dms != 0:
                    break
            else:
                groups_count += 1
                if groups_count == num_groups and num_groups != 0:
                    break
        assert dms_count <= GroupMe.GROUPS_PER_PAGE
        assert groups_count <= GroupMe.GROUPS_PER_PAGE

        # Trim data
        combined = combined[:(dms_count + groups_count)]

        # Increment offsets and pages
        if (dms_offset + dms_count) % GroupMe.DMS_PER_PAGE == 0:
            dms_offset = 0
            dms_page += 1
        else:
            dms_offset += dms_count

        if (groups_offset + groups_count) % GroupMe.GROUPS_PER_PAGE == 0:
            groups_offset = 0
            groups_page += 1
        else:
            groups_offset += groups_count

        new_page_token = '{}:{}-{}:{}'.format(dms_page, dms_offset,
                                              groups_page, groups_offset)

        return {'data': ConversationCollection(combined, new_page_token),
                'status': HTTP_200}

    def get_conversation(self, conversation_id, auth='', page=''):
        result = {'data': {}, 'status': HTTP_200} # TODO error handling

        if GroupMe._is_direct_message(conversation_id):
            # Expected conversation id: D + other user ID
            other_user_id = self._convo_to_groupme_id(conversation_id)

            dm_data = make_request(GroupMe.url_base, '/direct_messages',
                                   auth, {'other_user_id': other_user_id})

            # False only if there's a code error, _not_ user error
            assert other_user_id == dm_data['direct_messages']['recipient_id']

            result['data'] = Conversation(
                    cid=self._dm_to_convo_id(other_user_id),
                    name=dm_data['direct_messages']['name'],
                    last_updated=float(dm_data['direct_messages']['updated_at']))
        else:
            gid = self._convo_to_groupme_id(conversation_id)
            group_data = make_request(GroupMe.url_base,
                                      '/groups/{}'.format(gid), auth)
            result['data'] = Conversation(
                    cid=group_data['id'],
                    name=group_data['name'],
                    last_updated=float(group_data['updated_at']))

        return result

    def get_messages(self, conversation_id, auth='', page=''):
        result = {'data': {}, 'status': HTTP_200} # TODO error handling

        if GroupMe._is_direct_message(conversation_id):
            # Expected conversation id: D + other user ID
            other_user_id = self._convo_to_groupme_id(conversation_id)

            params = {'other_user_id': other_user_id}
            if page != '':
                # Groupme paging works by passing the last message ID
                # (...at this endpoint at least...)
                params['before_id'] = page

            dms = make_request(GroupMe.url_base, '/direct_messages',
                                   auth, params)
            messages = []
            for message in dms['direct_messages']:
                messages.append(Message(mid=message['id'],
                                      uid=message['user_id'],
                                      user_name=message['name'],
                                      text=message['text'],
                                      time=message['created_at']))
            if len(messages) > 0:
                last_id = messages[len(messages) - 1].mid
            else:
                last_id = ''
            result['data'] = MessageCollection(messages, next_page=last_id)

        else:
            gid = self._convo_to_groupme_id(conversation_id)

            params = {}
            if page != '':
                # Groupme paging works by passing the last message ID
                # (...at this endpoint at least...)
                params['before_id'] = page

            msgs = make_request(GroupMe.url_base,
                                      '/groups/{}/messages'.format(gid),
                                      auth, params)
            messages = []
            for message in msgs['messages']:
                messages.append(Message(mid=message['id'],
                                      uid=message['sender_id'],
                                      user_name=message['name'],
                                      text=message['text'],
                                      time=message['created_at']))
            if len(messages) > 0:
                last_id = messages[len(messages) - 1].mid
            else:
                last_id = ''
            result['data'] = MessageCollection(messages, next_page=last_id)

        return result


    def _is_direct_message(conversation_id: str) -> bool:
        return conversation_id.startswith(GroupMe.DM_ID_PREFIX)

    def _convo_to_groupme_id(cls, conversation_id: str) -> str:
        # Convert client-facing conversation_id into the format groupme expects
        return conversation_id[GroupMe.ID_PREFIX_LENGTH:]

    def _dm_to_convo_id(cls, other_user_id: str) -> str:
        # NOTE: We use the ID of the other user because of how groupme works
        return GroupMe.DM_ID_PREFIX + other_user_id

    def _group_to_convo_id(cls, group_id: str) -> str:
        return GroupMe.GROUP_ID_PREFIX + group_id
