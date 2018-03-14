import json

import falcon

class TestResource(object):

    def on_get(self, req, resp, service, id):
        doc = {'message': 'hello, world!', 'service': service}
        auth = req.get_param('token', default='')

        doc['auth'] = auth
        doc['id'] = id

        resp.body = json.dumps(doc)
        resp.status = falcon.HTTP_200 # 200 by default, leaving as an example
