from pathlib import Path
from types import SimpleNamespace
import CdbsModules.CdbsEvn as CdbsEvn
import CdbsModules.DataHandler as DataHandler
from CdbsModules.CdbsAuth import CdbsAuth
from CdbsModules.CdbsApi import CdbsApi
from CdbsModules.QueriesApi import QueriesApi
from CdbsModules.Translate import translate


g_selected_component_uuid: str = ''
g_selected_modification_uuid: str = ''
g_last_clicked_object: Path = Path('')

def update_components_list():
    """Create folders for all bookmark components of the current user"""
    library_path = Path(CdbsEvn.g_library_path)
    if not library_path.is_dir():
        DataHandler.logger(
            'warning',
            translate(
                'CadbaseMacro',
                'The path to the local library specified in the settings is missing (not found).',
            ),
        )
        return
    CdbsApi(QueriesApi.fav_components())
    data = DataHandler.parsing_gpl()
    if not isinstance(data, SimpleNamespace):
        DataHandler.logger(
            'warning',
            translate(
                'CadbaseMacro',
                'Received data about components is not suitable for processing',
            ),
        )
        return
    if not data.components:
        DataHandler.logger('warning', translate('CadbaseMacro', "You don't have favorite components"))
        return
    for component in data.components:
        DataHandler.logger(
            'log',
            translate('CadbaseMacro', 'Component UUID:')
            + f' {component.uuid}',
        )
        new_dir: Path = (
            library_path
            / f'{component.name} (from  {component.ownerUser.username})'
        )
        DataHandler.create_object_path(new_dir, component, 'component')
    DataHandler.logger('info', translate('CadbaseMacro', 'Component list update finished'))


def update_component():
    """Creating folders for all component modifications of current component"""
    if not g_selected_component_uuid:
        DataHandler.logger('warning', translate('CadbaseMacro', 'Not set UUID for select component'))
        return
    CdbsApi(QueriesApi.component_modifications(g_selected_component_uuid))
    data = DataHandler.parsing_gpl()
    if not isinstance(data, SimpleNamespace):
        DataHandler.logger(
            'warning',
            translate(
                'CadbaseMacro',
                'Received data about component is not suitable for processing'
            ),
        )
        return
    if not data.componentModifications:
        DataHandler.logger('warning', translate('CadbaseMacro', 'No modifications for the component'))
    for modification in data.componentModifications:
        new_dir = g_last_clicked_object / modification.modificationName
        DataHandler.create_object_path(new_dir, modification, 'modification')
    DataHandler.logger('info', translate('CadbaseMacro', 'Updated the list of component modifications'))


def update_component_modificaion():
    """Updating files on modification folder"""
    if not g_selected_modification_uuid:
        DataHandler.logger('warning', translate('CadbaseMacro', 'Not set UUID for select modification'))
        return
    CdbsApi(QueriesApi.target_fileset(g_selected_modification_uuid))
    data = DataHandler.parsing_gpl()
    if not isinstance(data, SimpleNamespace):
        DataHandler.logger('warning', translate('CadbaseMacro', 'Received data about fileset is not suitable for processing'))
        return
    if not data.componentModificationFilesets:
        DataHandler.logger('warning', translate('CadbaseMacro', 'Fileset not found for FreeCAD'))
        return
    CdbsApi(QueriesApi.fileset_files(data.componentModificationFilesets[0].uuid))
    data = DataHandler.parsing_gpl()
    if not isinstance(data, SimpleNamespace):
        DataHandler.logger(
            'warning',
            translate(
                'CadbaseMacro',
                'Received data about files of fileset is not suitable for processing',
            ),
        )
        return
    if not data.componentModificationFilesetFiles:
        DataHandler.logger('warning', translate('CadbaseMacro', 'No files in fileset'))
        return
    # necessary data to start downloading files
    urls = []  # for store pre-signed URLs for downloading files
    fns = []  # for store full patches with filenames
    for file_of_fileset in data.componentModificationFilesetFiles:
        urls.append(file_of_fileset.downloadUrl)
        fns.append(g_last_clicked_object / file_of_fileset.filename)
    inputs = zip(urls, fns)
    DataHandler.download_parallel(inputs)
    DataHandler.logger('info', translate('CadbaseMacro', 'Download file(s):') + f' {len(urls)}')
    DataHandler.logger('info', translate('CadbaseMacro', 'Component modification files update completed'))


def update_selected_object_uuid():
    """Upgrading selected uuid for a object, get data from user-selected a folder"""
    global g_selected_component_uuid
    global g_selected_modification_uuid
    # clearing old uuids
    g_selected_component_uuid = ''
    g_selected_modification_uuid = ''
    component_file = g_last_clicked_object / 'component'
    # check file with component info
    if component_file.exists():
        component_data = DataHandler.read_object_info(component_file, 'component')
        g_selected_component_uuid = component_data.uuid
        return
    modification_file = g_last_clicked_object / 'modification'
    # check file with modification info
    if modification_file.exists():
        modification_data = DataHandler.read_object_info(modification_file, 'modification')
        # save the uuid of the selected modification for uploading files
        g_selected_modification_uuid = modification_data.uuid
