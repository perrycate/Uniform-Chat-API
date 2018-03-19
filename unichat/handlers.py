import falcon

from unichat.models import User, jsonify
from unichat.translators import DummyTranslator


# TODO proper config file? enum?
SERVICES = ['dummy']

"""
Manages all incoming HTTP requests for conversations, invoking the
appropriate translator service.
"""
class ConversationsHandler(object):

    def __init__(self):
        self.dummy_translator = DummyTranslator()


    def on_get(self, req, resp, service, convo_id):
        auth = req.get_param('token', default='')

        ## Add other handlers here as they are created
        if service == 'dummy':
            result = self.dummy_translator.get_conversation(convo_id, auth)
        else:
            # No matching handler
            raise falcon.HTTPBadRequest

        resp.body = jsonify(result['data'])
        resp.status = result['status']


"""
Manages all incoming HTTP requests for users, invoking the appropriate
translator service.
"""
class UsersHandler(object):

    def __init__(self):
        self.dummy_translator = DummyTranslator()


    def on_get(self, req, resp, service, convo_id):
        auth = req.get_param('token', default='')

        ## Add other handlers here as they are created
        if service == 'dummy':
            result = self.dummy_translator.get_users(convo_id, auth)
        else:
            # No matching handler
            raise falcon.HTTPBadRequest

        resp.body = jsonify(result['data'])
        resp.status = result['status']


"""
Manages all incoming HTTP requests for users, invoking the appropriate
translator service.
"""
class MessagesHandler(object):

    def __init__(self):
        self.dummy_translator = DummyTranslator()


    def on_get(self, req, resp, service, convo_id):
        auth = req.get_param('token', default='')
        page = req.get_param('page', default='')

        ## Add other handlers here as they are created
        if service == 'dummy':
            result = self.dummy_translator.get_messages(convo_id, auth, page)
        else:
            # No matching handler
            raise falcon.HTTPBadRequest

        resp.body = jsonify(result['data'])
        resp.status = result['status']
