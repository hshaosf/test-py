"""Permit List module"""
import json
import falcon
import jsend
import sentry_sdk
from screendoor_sdk.screendoor import Screendoor

class PermitList():
    """Permit List class"""
    scrndr = None
    scrndr_proj_id = None

    def __init__(self):
        pass

    def init_screendoor(self, key, version, host, project_id):
        """initialize screendoor"""
        self.scrndr = Screendoor(key, version, host)
        self.scrndr_proj_id = project_id

    def get_permit_list(self, permit_type):
        """return list of permits"""
        params = {'per_page': 100, 'page' : 1}
        if permit_type == 'retail':
            # pylint: disable=line-too-long
            params['advanced_search'] = '%5B%7B"name"%3A"forms"%2C"method"%3A"is"%2C"value"%3A5804%7D%2C%7B"name"%3A"rfdd8a5g7g"%2C"method"%3A"is_any"%2C"value"%3A%5B"retailer+(medicinal+and+adult+use)"%2C"medicinal+retailer+(medicinal+only)"%2C"delivery+only+retailer+(medicinal+and+adult+use)"%5D%7D%5D'

        sd_responses = self.scrndr.get_project_responses(self.scrndr_proj_id, params, 500)

        if isinstance(sd_responses, list):
            sd_responses_context = {
                'length': len(sd_responses),
                'data': list(map(lambda x: x.get('sequential_id', ''), sd_responses))}
        else:
            sd_responses_context = sd_responses

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra('get_permit_list.sd_responses', sd_responses_context)

        return self.get_list_transform(sd_responses)

    def get_list_transform(self, sd_responses):
        """return a transformed list from screendoor reponses """
        permit_list = []
        responses_missing = []

        if isinstance(sd_responses, list):
            for resp in sd_responses:
                if resp.get('responses', False) and resp['responses'].get('dd8a5g7g', False):
                    resp_status = resp.get('status', '').upper()
                    item = {
                        'APPLICATION ID':'',
                        'DBA NAME':'',
                        'PARCEL':'',
                        'STATUS':resp_status,
                        'REFERRING DEPARTMENT':''
                    }
                    data = resp['responses']
                    item['APPLICATION ID'] = data.get('uqqrsogr', '')
                    item['DBA NAME'] = data.get('60w4ep9y', '')
                    item['PARCEL'] = data.get('kvrgbqrl', '')

                    if data['dd8a5g7g'] and data['dd8a5g7g']['checked']:
                        for applied_permit_type in data['dd8a5g7g']['checked']:
                            item[applied_permit_type.upper()] = resp_status

                    permit_list.append(item)
                else:
                    responses_missing.append(
                        {'id':resp['id'], 'sequential_id':resp['sequential_id']}
                    )

            with sentry_sdk.configure_scope() as scope:
                scope.set_extra('get_list_transform.permit_list_len', len(permit_list))
                if responses_missing:
                    scope.set_extra('get_list_transform.responses_missing', responses_missing)
        else:
            return False
        return permit_list

    def on_get(self, _req, resp, permit_type):
        """on GET request
        return list of permits
        """
        msg = False
        if permit_type == 'retail':
            permit_list = self.get_permit_list(permit_type)
            if isinstance(permit_list, list):
                msg = {'list': permit_list}
        else:
            pass

        if msg is not False:
            sentry_sdk.capture_message('success', 'info')
            resp.body = json.dumps(jsend.success(msg))
            resp.status = falcon.HTTP_200
        else:
            msg = 'ERROR'
            sentry_sdk.capture_message(msg, 'error')
            resp.body = json.dumps(jsend.error(msg))
            resp.status = falcon.HTTP_400
