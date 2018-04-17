"""
Translates incoming requests into proper queries against GroupMe's public API.
"""
from unichat.models import User, Conversation, ConversationCollection, \
                                Message, MessageCollection
from unichat.util import make_request
from unichat.translators import Translator


class GroupMe(Translator):

    URL_BASE = 'https://api.groupme.com/v3'
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
            other_user_id = self._convo_to_groupme_id(conversation_id)

            # Add other user
            dm_data = make_request(GroupMe.URL_BASE, '/direct_messages',
                                   auth, {'other_user_id': other_user_id})

            # Determine name of other person. Groupme never returns a DM, only
            # the messages, so we have to find a message _from_ the other
            # person
            other_user_name = ''
            for message in dm_data['direct_messages']:
                if message['sender_id'] == other_user_id:
                    other_user_name = message['name']

            members.append(User(uid=other_user_id, name=other_user_name))

            # Add ourselves
            self_data = make_request(GroupMe.URL_BASE, '/users/me', auth)
            members.append(User(uid=self_data['id'], name=self_data['name']))
        else:
            # Expected conversation id: G + group ID
            gid = self._convo_to_groupme_id(conversation_id)
            data = make_request(GroupMe.URL_BASE,
                                '/groups/{}'.format(gid), auth)
            for m in data['members']:
                members.append(User(uid=m['id'], name=m['nickname']))

        return members # TODO error handling

    def get_conversations_list(self, auth='', page='1:0-1:0'):

        # Page token format: '(DM Page):(DM Index)-(Groups Page):(Groups index)
        dms, groups = page.split('-')
        dms_page, dms_offset = [int(x) for x in dms.split(':')]
        groups_page, groups_offset = [int(x) for x in groups.split(':')]

        # Retrieve direct messages, convert to Conversations
        dms = []
        dms_raw = make_request(
            GroupMe.URL_BASE, '/chats', auth,
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
            GroupMe.URL_BASE, '/groups', auth,
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
        return ConversationCollection(combined, new_page_token)

    def get_conversation(self, conversation_id, auth=''):
        if GroupMe._is_direct_message(conversation_id):
            # Expected conversation id: D + other user ID
            other_user_id = self._convo_to_groupme_id(conversation_id)

            dm_data = make_request(GroupMe.URL_BASE, '/direct_messages',
                                   auth, {'other_user_id': other_user_id})

            # Determine name of other person. Groupme never returns a DM, only
            # the messages, so we have to find a message _from_ the other
            # person
            other_user_name = ''
            for message in dm_data['direct_messages']:
                if message['sender_id'] == other_user_id:
                    other_user_name = message['name']


            return Conversation(
                    cid=self._dm_to_convo_id(other_user_id),
                    name=other_user_name,
                    last_updated=float(
                            dm_data['direct_messages'][0]['created_at']))
        else:
            gid = self._convo_to_groupme_id(conversation_id)
            group_data = make_request(GroupMe.URL_BASE,
                                      '/groups/{}'.format(gid), auth)
            return Conversation(
                    cid=group_data['id'],
                    name=group_data['name'],
                    last_updated=float(group_data['updated_at']))

    def get_messages(self, conversation_id, auth='', page=''):
        if GroupMe._is_direct_message(conversation_id):
            # Expected conversation id: D + other user ID
            other_user_id = self._convo_to_groupme_id(conversation_id)

            params = {'other_user_id': other_user_id}
            if page != '':
                # Groupme paging works by passing the last message ID
                # (...at this endpoint at least...)
                params['before_id'] = page

            dms = make_request(GroupMe.URL_BASE, '/direct_messages',
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

            return MessageCollection(messages, next_page=last_id)

        else:
            gid = self._convo_to_groupme_id(conversation_id)

            params = {}
            if page != '':
                # Groupme paging works by passing the last message ID
                # (...at this endpoint at least...)
                params['before_id'] = page

            msgs = make_request(GroupMe.URL_BASE,
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

            return MessageCollection(messages, next_page=last_id)


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
