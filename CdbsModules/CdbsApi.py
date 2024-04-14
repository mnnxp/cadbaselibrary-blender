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
            translate('CdbsApi', 'for correct operation of the macro it is necessary to free the path')
            + f' {CdbsEvn.g_response_path}'
            + ' or change the location of the local library')
        return
    if DataHandler.handle_response(reply):
        if CdbsEvn.g_response_path.is_file():
            DataHandler.remove_object(CdbsEvn.g_response_path)  # deleting old a response if it exists
        with CdbsEvn.g_response_path.open('wb') as fd:
            for chunk in reply.iter_content(chunk_size=128):
                fd.write(chunk)
        logger('debug', translate('CdbsApi', 'Successful processing request'))
    else:
        logger('error', translate('CdbsApi', 'Failed processing request'))


class CdbsApi:
    """Sending a request to the CADBase API and processing the response"""

    def __init__(self, query):
        logger('debug', translate('CdbsApi', 'API Point:') + f' {CdbsEvn.g_cdbs_api}')
        if not CdbsEvn.g_auth_token:
            logger('error', translate('CdbsApi', 'Token not found. Please get a new token and try again'))
            return
        logger('debug', translate('CdbsApi', 'Getting data...'))
        try:
            auth_header = 'Bearer ' + CdbsEvn.g_auth_token
            headers = {
                'Content-Type': CdbsEvn.g_content_type,
                'Authorization': auth_header.encode()}
            body = json.dumps(query).encode('utf-8')
            logger('log', translate('CdbsApi', 'Query include body:') + f' {body}')
            reply = requests.post(CdbsEvn.g_cdbs_api, headers=headers, data=body)
        except Exception as e:
            logger(
                'error',
                translate('CdbsApi', 'Exception when trying to sending the request:')
                + f' {e}'),
        else:
            parsing_response(reply)
