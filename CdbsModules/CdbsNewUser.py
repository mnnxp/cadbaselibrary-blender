""" This file contains one class for authorization on the CADBase platform """

from pathlib import Path
import CdbsModules.CdbsEvn as CdbsEvn
from CdbsModules.CdbsAuth import CdbsAuth
from CdbsModules.CdbsApi import CdbsApi
from CdbsModules.QueriesApi import QueriesApi
import CdbsModules.DataHandler as DataHandler
import CdbsModules.PartsList as PartsList
from CdbsModules.Translate import translate
from CdbsModules.Logger import logger


def register_new_user():
    cdbs_prefs = CdbsEvn.get_preferences()
    if not cdbs_prefs:
        logger('debug', translate('cdbs', 'Preferences not found.'))
        return
    if not CdbsEvn.check_online_access():
        return
    # update the settings so that user changes are not lost
    CdbsEvn.update_settings()
    PartsList.g_last_clicked_object = Path(CdbsEvn.g_library_path)
    if cdbs_prefs.username and cdbs_prefs.password:
        CdbsRegUser(cdbs_prefs.username, cdbs_prefs.password)
        CdbsAuth(cdbs_prefs.username, cdbs_prefs.password)


class CdbsRegUser:
    """Register a new user the CADBase platform"""

    def __init__(self, username, password):
        logger('debug', translate('cdbs', 'API Point:') + f' {CdbsEvn.g_cdbs_api}')
        logger('message', translate('cdbs', 'New user registration, please wait.'))
        if not CdbsApi(QueriesApi.register_user(username, password), skip_token=True):
            return
        self.fileset_uuid = DataHandler.deep_parsing_gpl('registerUser')
        logger(
            'log',
            translate('cdbs', 'New user UUID:') + f' {self.fileset_uuid}',
        )
