import falcon

from unichat.handlers import ConversationsList, Conversation, Users, Messages
from unichat.translators import Dummy, GroupMe


translator_map = {
    'dummy': Dummy(),
    'groupme': GroupMe(),
}

api = application = falcon.API()
api.add_route('/{service}/conversations',
              ConversationsList(translator_map))
api.add_route('/{service}/conversations/{convo_id}',
              Conversation(translator_map))
api.add_route('/{service}/conversations/{convo_id}/users',
              Users(translator_map))
api.add_route('/{service}/conversations/{convo_id}/messages',
              Messages(translator_map))
