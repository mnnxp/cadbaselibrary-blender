from pathlib import Path
from types import SimpleNamespace
import CdbsModules.CdbsEvn as CdbsEvn
import CdbsModules.DataHandler as DataHandler
from CdbsModules.CdbsApi import CdbsApi
from CdbsModules.QueriesApi import QueriesApi
from CdbsModules.Translate import translate
from CdbsModules.Logger import logger


g_selected_component_uuid: str = ''
g_selected_modification_uuid: str = ''
g_last_clicked_object: Path = Path(CdbsEvn.g_library_path)
g_current_position = 'Components (parts)'

def update_components_list():
    """Create folders for all bookmark components of the current user"""
    library_path = Path(CdbsEvn.g_library_path)
    if not library_path.is_dir():
        logger(
            'error',
            translate('cdbs', 'The path to the local library specified is missing (set in the settings).')
        )
        return
    if not CdbsApi(QueriesApi.fav_components()):
        return
    data = DataHandler.parsing_gpl()
    if not isinstance(data, SimpleNamespace):
        logger(
            'warning',
            translate('cdbs', 'Received data about components is not suitable for processing')
        )
        return
    if not data.components:
        logger('info', translate('cdbs', "You don't have favorite components"))
        return
    for component in data.components:
        logger(
            'log',
            translate('cdbs', 'Component UUID:')
            + f' {component.uuid}',
        )
        new_dir: Path = (
            library_path
            / f'{component.name} (@{component.ownerUser.username})'
        )
        DataHandler.create_object_path(new_dir, component, 'component')
    logger('info', translate('cdbs', 'Component list update finished.'))


def update_component():
    """Creating folders for all component modifications of current component"""
    if not g_selected_component_uuid:
        logger('warning', translate('cdbs', 'Not set UUID for select component.'))
        return
    if not CdbsApi(QueriesApi.component_modifications(g_selected_component_uuid)):
        return
    data = DataHandler.parsing_gpl()
    if not isinstance(data, SimpleNamespace):
        logger(
            'warning',
            translate('cdbs', 'Received data about component is not suitable for processing.')
        )
        return
    if not data.componentModifications:
        logger('warning', translate('cdbs', 'No modifications for the component.'))
    for modification in data.componentModifications:
        new_dir = g_last_clicked_object / modification.modificationName
        DataHandler.create_object_path(new_dir, modification, 'modification')
    logger('info', translate('cdbs', 'The list of modifications to the component has been updated.'))


def update_component_modificaion():
    """Updating files on modification folder"""
    if not g_selected_modification_uuid:
        logger('warning', translate('cdbs', 'Not set UUID for select modification.'))
        return
    if not CdbsApi(QueriesApi.target_fileset(g_selected_modification_uuid)):
        return
    data = DataHandler.parsing_gpl()
    if not isinstance(data, SimpleNamespace):
        logger('warning', translate('cdbs', 'Received data about fileset is not suitable for processing.'))
        return
    if not data.componentModificationFilesets:
        logger('warning', translate('cdbs', 'Fileset not found for Blender.'))
        return
    if not CdbsApi(QueriesApi.fileset_files(data.componentModificationFilesets[0].uuid)):
        return
    data = DataHandler.parsing_gpl()
    if not isinstance(data, SimpleNamespace):
        logger(
            'warning',
            translate('cdbs', 'Received data about files of fileset is not suitable for processing.')
        )
        return
    if not data.componentModificationFilesetFiles:
        logger('warning', translate('cdbs', 'No files in fileset.'))
        return
    # necessary data to start downloading files
    urls = []  # for store pre-signed URLs for downloading files
    fns = []  # for store full patches with filenames
    for file_of_fileset in data.componentModificationFilesetFiles:
        urls.append(file_of_fileset.downloadUrl)
        fns.append(g_last_clicked_object / file_of_fileset.filename)
    inputs = zip(urls, fns)
    DataHandler.download_parallel(inputs)
    logger('info', translate('cdbs', 'Download file(s):') + f' {len(urls)}')
    logger('info', translate('cdbs', 'The set of files for the component modification has been updated.'))


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

def detect_current_position():
    global g_current_position

    if len(CdbsEvn.g_library_path) < 2:
        logger('warning', translate('cdbs', 'Please specify path to the local library in CADBase Library (addon) settings.'))
        return 'ERROR'
    if not Path(CdbsEvn.g_library_path).is_dir():
        logger('info', translate('cdbs', 'Need set correct settings:') + f' {CdbsEvn.g_library_path}')
        return 'UNKNOWN'
    if g_last_clicked_object == Path(CdbsEvn.g_library_path):
        g_current_position = 'Components (parts)'
        return 'TREE'  # show components
    component_file = g_last_clicked_object / 'component'
    if component_file.exists():
        g_current_position = translate('cdbs', 'Component:') + f' {g_last_clicked_object.name}'
        return 'COMPONENT'  # show modifications of component
    modification_file = g_last_clicked_object / 'modification'
    if modification_file.exists():
        # g_current_position = 'fileset (Blender)'
        g_current_position = translate('cdbs', 'Modification:') + f' {g_last_clicked_object.parent.name}'
        return 'MODIFICATION'  # show fileset for Blender of modification
    return 'UNKNOWN'