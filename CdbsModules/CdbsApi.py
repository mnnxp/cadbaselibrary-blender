""" Functionality for processing requests to the CADBase platform """

import requests
import json
from pathlib import Path
import CdbsModules.CdbsEvn as CdbsEvn
import CdbsModules.DataHandler as DataHandler
from CdbsModules.Translate import translate
from CdbsModules.Logger import logger


def parsing_response(reply):
    if CdbsEvn.g_response_path.is_dir():
        logger(
            'error',
            translate('cdbs', 'For correct operation of the addon it is necessary to free the path \
or change the location of the local library. Path:')
            + f' {CdbsEvn.g_response_path}')
        return
    if DataHandler.handle_response(reply):
        if CdbsEvn.g_response_path.is_file():
            DataHandler.remove_object(CdbsEvn.g_response_path)  # deleting old a response if it exists
        with CdbsEvn.g_response_path.open('wb') as fd:
            for chunk in reply.iter_content(chunk_size=128):
                fd.write(chunk)
        logger('debug', translate('cdbs', 'Successful processing request.'))
    else:
        logger('error', translate('cdbs', 'Failed processing request.'))


class CdbsApi:
    """Sending a request to the CADBase API and processing the response"""

    def __init__(self, query):
        logger('debug', translate('cdbs', 'API Point:') + f' {CdbsEvn.g_cdbs_api}')
        if not CdbsEvn.g_auth_token:
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
                + f' {e}'),
        else:
            parsing_response(reply)
