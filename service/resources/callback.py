"""Callback example module"""
import json
import falcon
import jsend

class Callback():
    """Callback class"""
    def on_get(self, _req, resp, name):
        """on get request
        return Callback message
        """
        msg = {'message': 'Callback'}
        if name == 'auth':
            msg = {'message': 'Auth Callback'}
        resp.body = json.dumps(jsend.success(msg))
        resp.status = falcon.HTTP_200
