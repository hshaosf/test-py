"""Datastore example module"""
import json
import os
import falcon
import jsend
from screendoor_sdk.screendoor import Screendoor


class Datastore():
    """Callback class"""
    scrndr = None

    def on_get(self, _req, resp, method):
        """on get request
        return Datastore message
        """
        msg = {'message': 'Datastore'}
        if (self.is_auth()
                and hasattr(self.__class__, method)
                and callable(getattr(self.__class__, method))):
            dispatch = getattr(self, method)
            if method.startswith('screendoor_'):
                sd_key = os.environ['SD_KEY']
                self.scrndr = Screendoor(sd_key)
            msg = dispatch(_req, resp)

        resp.body = json.dumps(jsend.success(msg))
        resp.status = falcon.HTTP_200

    @staticmethod
    def is_auth():
        """ is authenticated """
        return True

    def screendoor_get_project(self, _req, _resp):
        """ get part one from screendoor """
        project_id = os.environ['SD_PROJECT_ID']
        form_id = os.environ['SD_FORM_ID']
        param = {'per_page': 100, 'page' : 1}
        param['advanced_search'] = '%5B%7B"name"%3A"form"%2C"placeholder"%3Anull%2C"method"%3A"is"%2C"value"%3A'+str(form_id)+'%7D%5D'
        items = {'items':[]}
        sd_responses = self.scrndr.get_project_responses(project_id, param, 1)
        if isinstance(sd_responses, list):
            for i, resp in enumerate(sd_responses):
                resp = self.etl_project_resp(resp)
                sd_responses[i] = resp
            items['items'] = sd_responses
        return items

    @staticmethod
    def etl_project_resp(sd_resp):
        """ do ETL for part one screendoor response """
        app_id = str(sd_resp.get('uqqrsogr') or '')
        if not app_id:
            app_id = 'P-' + str(sd_resp['id'])
        sd_resp['application_id'] = app_id

        return sd_resp



    