import json

import falcon

from .handlers import DummyHandler


# TODO proper config file? enum?
SERVICES = ['dummy']


class ConversationsResource(object):

    def __init__(self):
        self.dummy_handler = DummyHandler()


    def on_get(self, req, resp, service, convo_id):
        auth = req.get_param('token', default='')

        ## Add other handlers here as they are created
        if service == 'dummy':
        	result = self.dummy_handler.handle_request(convo_id)
        else:
            # No matching handler
            raise falcon.HTTPBadRequest

        resp.body = json.dumps(result['data'])
        resp.status = result['status']
