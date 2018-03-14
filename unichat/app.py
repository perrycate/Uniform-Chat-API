import falcon

from .handlers import ConversationsHandler, UsersHandler, MessagesHandler

api = application = falcon.API()
api.add_route('/{service}/conversations/{convo_id}', ConversationsHandler())
api.add_route('/{service}/conversations/{convo_id}/users', UsersHandler())
api.add_route('/{service}/conversations/{convo_id}/messages', MessagesHandler())
# TODO route to discover conversations
