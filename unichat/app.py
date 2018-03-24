import falcon

from unichat.handlers import ConversationsHandler, UsersHandler, MessagesHandler
from unichat.translators import DummyTranslator


translator_map = {
    'dummy': DummyTranslator()
}

api = application = falcon.API()
api.add_route('/{service}/conversations/{convo_id}',
              ConversationsHandler(translator_map))
api.add_route('/{service}/conversations/{convo_id}/users',
              UsersHandler(translator_map))
api.add_route('/{service}/conversations/{convo_id}/messages',
              MessagesHandler(translator_map))
# TODO route to discover conversations
