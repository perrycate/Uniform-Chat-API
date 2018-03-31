"""
Handles outgoing requests to a particular service. Accepts given parameters,
makes whatever request(s) is necessary to the corresponding service, and returns
data in a uniform format.
"""
from abc import ABC, abstractmethod


class Translator(ABC):

    @abstractmethod
    def get_conversations_list(self, auth, page):
        pass

    @abstractmethod
    def get_users(self, conversation_id, auth, page):
        pass

    @abstractmethod
    def get_conversation(self, conversation_id, auth, page):
        pass

    @abstractmethod
    def get_messages(self, conversation_id, auth, page):
        pass
