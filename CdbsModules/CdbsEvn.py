"""Global variables of the addon are collected here"""

import pathlib
import bpy
from CdbsModules.Logger import logger


g_cadbase_api = 'https://api.cadbase.rs'  # default CADBase platform point
cdbs_settings_file = pathlib.Path() / 'cadbase_library' / 'cdbs_preferences.dat'
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
g_response_path = pathlib.Path() / g_resp_file
g_log_file_path = pathlib.Path() / g_resp_file / '.log'
g_stack_event = []  # contains messages to be displayed to the user

class EventMessage():
    """Stores the message and the level of importance of that message"""

    def __init__(self, level, msg):
        self.level = level
        self.msg = msg

def update_api_points():
    global g_api_login
    global g_cdbs_api
    g_api_login = f'{g_base_api}/login'
    g_cdbs_api = f'{g_base_api}/graphql'

def save():
    with open(cdbs_settings_file, "w", encoding='utf-8') as f:
        f.write(f'{g_library_path.strip()}\n{g_base_api.strip()}\n{g_auth_token.strip()}')
    logger('debug', f'3 {g_library_path}\n{g_base_api}\n{g_auth_token}')
    logger('debug', 'Configuration updated OK')

def update_settings():
    global g_library_path
    global g_base_api
    global g_auth_token
    global g_response_path
    global g_log_file_path
    if cdbs_settings_file.is_file():
        with open(cdbs_settings_file, 'r') as settings_data:
            g_library_path = settings_data.readline().strip()   # 1th line
            g_base_api = settings_data.readline().strip()       # 2th line
            g_auth_token = settings_data.readline().strip()     # 3th line
        update_api_points()
        if pathlib.Path(g_library_path).is_dir():
            g_response_path = pathlib.Path(g_library_path) / g_resp_file
            g_log_file_path = g_response_path.with_suffix('.log')

update_settings()