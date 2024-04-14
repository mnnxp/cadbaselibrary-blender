""" This file contains one class for authorization on the CADBase platform """

import requests
import json
import CdbsModules.DataHandler as DataHandler
import CdbsModules.CdbsEvn as CdbsEvn
from CdbsModules.Translate import translate
from CdbsModules.Logger import logger


def parsing_response(reply):
    if DataHandler.handle_response(reply):
        token = json.loads(str(reply.content, 'utf-8'))
        CdbsEvn.g_auth_token = token['bearer']
        CdbsEvn.save()
        logger('info', translate('CdbsAuth', 'Successful authorization'))
    else:
        logger('error', translate('CdbsAuth', 'Failed authorization'))


class CdbsAuth:
    """Getting a token to access the CADBase platform"""

    def __init__(self, username, password):
        logger(
            'message',
            translate('CdbsAuth', 'Getting a new token, please wait.'),
        )
        self.query = {'user': {'username': username, 'password': password}}
        try:
            headers = {'Content-Type': CdbsEvn.g_content_type}
            body = json.dumps(self.query).encode('utf-8')
            reply = requests.post(CdbsEvn.g_api_login, headers=headers, data=body)
            del body
            del self.query
        except Exception as e:
            logger(
                'error',
                translate('CdbsAuth', 'Exception when trying to login:')
                + f' {e}',
            )
        else:
            parsing_response(reply)
