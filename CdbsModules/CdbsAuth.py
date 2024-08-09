""" This file contains one class for authorization on the CADBase platform """

import requests
import json
from . import DataHandler as DataHandler
from . import CdbsEvn as CdbsEvn
from .Translate import translate
from .Logger import logger


def parsing_response(reply):
    if DataHandler.handle_response(reply):
        token = json.loads(str(reply.content, 'utf-8'))
        CdbsEvn.g_auth_token = token['bearer']
        CdbsEvn.save()
        logger('info', translate('cdbs', 'Successful authorization.'))
    else:
        logger('error', translate('cdbs', 'Failed authorization.'))


class CdbsAuth:
    """Getting a token to access the CADBase platform"""

    def __init__(self, username, password):
        DataHandler.remove_object(CdbsEvn.g_response_path)  # deleting old a response if it exists
        if not DataHandler.check_online_access():
            return
        logger('debug', translate('cdbs', 'API Point:') + f' {CdbsEvn.g_api_login}')
        logger('message', translate('cdbs', 'Getting a new token, please wait.'))
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
                translate('cdbs', 'Exception when trying to login:')
                + f' {e}',
            )
        else:
            parsing_response(reply)
