"""Global variables of the addon are collected here"""

from pathlib import Path
import bpy
from .Translate import translate


g_base_package = ''
g_cadbase_api = 'https://api.cadbase.rs'  # default CADBase platform point
g_library_path = '' # for save the path to the local CADBase library
g_base_api = g_cadbase_api
g_api_login = f'{g_base_api}/login'
g_cdbs_api = f'{g_base_api}/graphql'
g_auth_token = ''
g_program_id = 53  # this is Blender ID in CADBase
g_user_agent = b'Mozilla/5.0 (Macintosh; Intel Mac OS 10 12.3; rv:42.0) \
                Gecko/20100101 Firefox/42.0'
g_content_type = b'application/json'
g_len_uuid = 36  # for a little uuid validation
g_program_name = 'Blender'
# Please don't use this name as the name of files or folders in the CADBase Library folder.
g_resp_file = 'cadbase_file_2018'
g_response_path = Path() / g_resp_file
g_log_file_path = Path() / g_resp_file / '.log'
g_stack_event = []  # contains messages to be displayed to the user
g_resetpoint_flag = False  # flag to reset the api point to the default value
g_resetcommitmsg_flag = False  # flag to reset the commit message for uploaded files
g_skip_blake3 = True  # hash reconciliation of files is enabled by default
g_force_upload = True  # forced updating of existing files is enabled by default


def get_preferences():
    return bpy.context.preferences.addons[g_base_package].preferences

def update_api_points(new_url):
    global g_base_api
    global g_api_login
    global g_cdbs_api
    g_base_api = new_url
    g_api_login = f'{g_base_api}/login'
    g_cdbs_api = f'{g_base_api}/graphql'

def save():
    cdbs_prefs = get_preferences()
    cdbs_prefs.api_key = g_auth_token
    cdbs_prefs.base_api = g_base_api
    cdbs_prefs.library_path = g_library_path
    cdbs_prefs.skip_blake3 = g_skip_blake3
    cdbs_prefs.force_upload = g_force_upload

def update_settings():
    global g_library_path
    global g_auth_token
    global g_response_path
    global g_log_file_path
    global g_skip_blake3
    global g_force_upload
    cdbs_prefs = get_preferences()
    if not cdbs_prefs:
        return False
    g_auth_token = cdbs_prefs.api_key
    if g_base_api != cdbs_prefs.base_api:
        update_api_points(cdbs_prefs.base_api)
    g_library_path = cdbs_prefs.library_path
    if Path(g_library_path).is_dir():
        g_response_path = Path(g_library_path) / g_resp_file
        g_log_file_path = g_response_path.with_suffix('.log')
    g_skip_blake3 = cdbs_prefs.skip_blake3
    g_force_upload = cdbs_prefs.force_upload
    return True