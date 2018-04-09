import falcon

import unichat.errors

from unichat.handlers import ConversationsList, Conversation, Users, Messages
from unichat.translators import Dummy, GroupMe, Slack


# Which translator to use for each service. /dummy/* is handled by Dummy(), etc
translator_map = {
    'dummy': Dummy(),
    'groupme': GroupMe(),
    'slack': Slack(),
}

# Set up Falcon Resources (from handlers.py) for each endpoint.
api = application = falcon.API()
api.add_route('/{service}/conversations',
              ConversationsList(translator_map))
api.add_route('/{service}/conversations/{convo_id}',
              Conversation(translator_map))
api.add_route('/{service}/conversations/{convo_id}/users',
              Users(translator_map))
api.add_route('/{service}/conversations/{convo_id}/messages',
              Messages(translator_map))

# Set up error handling
unichat.errors.set_mappings(api)
