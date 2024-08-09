"""Functionality for processing requests to the storage (S3) of CADBase platform"""

import requests
from . import DataHandler as DataHandler
from .Translate import translate
from .Logger import logger


class CdbsStorageApi:
    """Sending a file to CADBase storage and handling response (empty response - good case)"""

    def __init__(self, presigned_url, file_path):
        logger('message', translate('cdbs', 'Preparing for upload file...'))
        try:
            with open(file_path.absolute().as_posix(), 'rb') as target_file:
                logger('debug', translate('cdbs', 'Upload file...'))
                reply = requests.put(presigned_url, data=target_file)
        except Exception as e:
            logger(
                'error',
                translate('cdbs', 'Exception in upload file:')
                + f' {e}',
            )
        else:
            logger('log', translate('cdbs', 'File uploaded. Response bytes:'))
            DataHandler.handle_response(reply)
