from typing import Mapping

import falcon

from unichat.models import User, jsonify
from unichat.translators import Translator


"""
Manages incoming HTTP requests to discover conversations, invoking the
appropriate translator service.
"""
class ConversationsList(object):

    def __init__(self, translators: Mapping[str, Translator]) -> None:
        self.translators = translators


    def on_get(self, req, resp, service, convo_id):
        auth = req.get_param('token', default='')

        # Make sure request is for a valid service
        if service not in self.translators:
            raise falcon.HTTPBadRequest

        result = self.translators[service].get_conversations(convo_id, auth)

        resp.body = jsonify(result['data'])
        resp.status = result['status']


"""
Manages incoming HTTP requests for data on a specific conversation, invoking
the appropriate translator service.
"""
class Conversation(object):

    def __init__(self, translators: Mapping[str, Translator]) -> None:
        self.translators = translators


    def on_get(self, req, resp, service, convo_id):
        auth = req.get_param('token', default='')

        # Make sure request is for a valid service
        if service not in self.translators:
            raise falcon.HTTPBadRequest

        result = self.translators[service].get_conversation(convo_id, auth)

        resp.body = jsonify(result['data'])
        resp.status = result['status']


"""
Manages all incoming HTTP requests for users, invoking the appropriate
translator service.
"""
class Users(object):

    def __init__(self, translators: Mapping[str, Translator]) -> None:
        self.translators = translators


    def on_get(self, req, resp, service, convo_id):
        auth = req.get_param('token', default='')

        # Make sure request is for a valid service
        if service not in self.translators:
            raise falcon.HTTPBadRequest

        result = self.translators[service].get_users(convo_id, auth)

        resp.body = jsonify(result['data'])
        resp.status = result['status']


"""
Manages all incoming HTTP requests for users, invoking the appropriate
translator service.
"""
class Messages(object):

    def __init__(self, translators: Mapping[str, Translator]) -> None:
        self.translators = translators


    def on_get(self, req, resp, service, convo_id):
        auth = req.get_param('token', default='')
        page = req.get_param('page', default='')

        # Make sure request is for a valid service
        if service not in self.translators:
            raise falcon.HTTPBadRequest

        result = self.translators[service].get_messages(convo_id, auth, page)

        resp.body = jsonify(result['data'])
        resp.status = result['status']
