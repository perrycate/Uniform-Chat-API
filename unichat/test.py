import json

import falcon

class Resource(object):

    def on_get(self, req, resp):
        doc = {'message': 'hello, world!'}
        resp.body = json.dumps(doc)
        resp.status = falcon.HTTP_200 # 200 by default, leaving as an example
