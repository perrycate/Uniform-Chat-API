import json

def jsonify(model):

    if isinstance(model, list):
        rendered = [x.render() for x in model]
    else:
        rendered = model.render()

    return json.dumps(rendered)


class User(object):

    def __init__(self,uid, name):
        self.uid = uid
        self.name = name

    def render(self):
        return {
            'id': self.uid,
            'name': self.name
        }


class Conversation(object):

    def __init__(self, cid, name, last_updated):
        self.cid = cid
        self.name = name
        self.last_updated = last_updated

    def render(self):
        return {
            'id': self.cid,
            'name': self.name,
            'last_updated': self.last_updated,
        }


class ConversationCollection(object):

    def __init__(self, conversations, next_page):
        self.conversations = conversations
        self.next_page = next_page

    def render(self):
        return {
            'conversations': [c.render() for c in self.conversations],
            'nextPage': self.next_page
        }


class Message(object):

    def __init__(self, mid, uid, user_name, text, time, attachments=[]):
        self.mid = mid
        self.uid = uid
        self.user_name = user_name
        self.text = text
        self.attachments = attachments
        self.time = time

    def render(self):
        return {
            'id': self.mid,
            'userId': self.uid,
            'userName': self.user_name,
            'text': self.text,
            'attachments': [], #TODO Implement attachments
            'time': self.time
        }


class MessageCollection(object):
    def __init__(self, messages, next_page):
        self.messages = messages
        self.next_page = next_page

    def render(self):
        return {
            'messages': [m.render() for m in self.messages],
            'nextPage': self.next_page

        }
