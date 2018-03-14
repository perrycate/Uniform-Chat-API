import falcon

from .conversations import ConversationsResource

api = application = falcon.API()

api.add_route('/{service}/conversations/{convo_id}', ConversationsResource())
