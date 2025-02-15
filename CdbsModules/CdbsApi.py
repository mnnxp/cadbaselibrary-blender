""" Functionality for processing requests to the CADBase platform """

import requests
import json
from pathlib import Path
from . import CdbsEvn as CdbsEvn
from . import DataHandler as DataHandler
from .Translate import translate
from .Logger import logger


def parsing_response(reply):
    if CdbsEvn.g_response_path.is_dir():
        logger(
            'error',
            translate('cdbs', 'For correct operation of the addon it is necessary to free the path \
or change the location of the local library. Path:')
            + f' {CdbsEvn.g_response_path}')
        return False
    if DataHandler.handle_response(reply):
        with CdbsEvn.g_response_path.open('wb') as fd:
            for chunk in reply.iter_content(chunk_size=128):
                fd.write(chunk)
        logger('debug', translate('cdbs', 'Successful processing request.'))
        return True
    else:
        logger('error', translate('cdbs', 'Failed processing request.'))
    return False


class CdbsApi:
    """Sending a request to the CADBase API and processing the response"""

    def __init__(self, query, skip_token=False):
        DataHandler.remove_object(CdbsEvn.g_response_path)  # deleting old a response if it exists
        if not DataHandler.check_online_access():
            return
        logger('debug', translate('cdbs', 'API Point:') + f' {CdbsEvn.g_cdbs_api}')
        if not CdbsEvn.g_auth_token and not skip_token:
            logger('error', translate('cdbs', 'Token not found. Please get a new token and try again.'))
            return
        logger('debug', translate('cdbs', 'Getting data...'))
        try:
            auth_header = 'Bearer ' + CdbsEvn.g_auth_token
            headers = {
                'Content-Type': CdbsEvn.g_content_type,
                'Authorization': auth_header.encode()}
            body = json.dumps(query).encode('utf-8')
            logger('log', translate('cdbs', 'Query include body:') + f' {body}')
            reply = requests.post(CdbsEvn.g_cdbs_api, headers=headers, data=body)
        except Exception as e:
            logger(
                'error',
                translate('cdbs', 'Exception when trying to sending the request:')
                + f' {e}')
        else:
            parsing_response(reply)
