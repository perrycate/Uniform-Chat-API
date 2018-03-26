import falcon

from unichat.handlers import ConversationsListHandler, ConversationHandler, UsersHandler, MessagesHandler
from unichat.translators import DummyTranslator, GroupMeTranslator


translator_map = {
    'dummy': DummyTranslator(),
    'groupme': GroupMeTranslator(),
}

api = application = falcon.API()
api.add_route('/{service}/conversations',
              ConversationsListHandler(translator_map))
api.add_route('/{service}/conversations/{convo_id}',
              ConversationHandler(translator_map))
api.add_route('/{service}/conversations/{convo_id}/users',
              UsersHandler(translator_map))
api.add_route('/{service}/conversations/{convo_id}/messages',
              MessagesHandler(translator_map))
