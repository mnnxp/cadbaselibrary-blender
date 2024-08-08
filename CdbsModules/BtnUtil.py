from pathlib import Path
import bpy
from CdbsModules.CdbsStorage import CdbsStorage
import CdbsModules.CdbsEvn as CdbsEvn
import CdbsModules.PartsList as PartsList
from CdbsModules.Translate import translate
from CdbsModules.Logger import logger

g_tree_elements = []

def check_list_idx():
    """Checks whether the leaf exists and whether the index is outside the array boundary."""

    if not bpy.context.scene.cdbs_list:
        logger('warning', translate('cdbs', 'Target list not found.'))
        return False
    if bpy.context.scene.cdbs_list_idx >= len(bpy.context.scene.cdbs_list):
        logger('warning', translate('cdbs', 'Target index not found:') + f' {bpy.context.scene.cdbs_list_idx}')
        return False
    return True

def push_files_of_fileset():
    """Starts processing and sending files from the local file set to the cloud if a modification file set is open."""

    current_position = PartsList.detect_current_position()
    if not current_position == 'MODIFICATION':
        logger('warning', translate('cdbs', 'Need open modification, now:') + f' {current_position}')
        return
    PartsList.update_selected_object_uuid()
    arg = (
        PartsList.g_selected_modification_uuid,
        PartsList.g_last_clicked_object)
    CdbsStorage(arg)

#-----------------------------------------------------------------------------
#
# https://docs.blender.org/api/current/bpy.types.BlendDataLibraries.html#bpy.types.BlendDataLibraries.load
# Returns a context manager which exposes 2 library objects on entering.
# Each object has attributes matching bpy.data which are lists of strings to be linked.
def link_file_objects():
    """Links all objects of the selected file using _BlendDataLibraries.load_."""

    if not check_list_idx():
        return
    filepath = Path(bpy.context.scene.cdbs_list[bpy.context.scene.cdbs_list_idx].path)
    if Path(bpy.data.filepath) == filepath:
        logger('warning', translate('cdbs', "You can't create a link to a file because it's already open."))
        return
    if not filepath.exists():
        logger('warning', translate('cdbs', 'Skip (file path does not exist):' + f' {filepath.name}'))
        return
    if not filepath.suffix == '.blend':
        logger('warning', translate('cdbs', 'Skip:') + f' {filepath.name}')
        return
    # link all objects
    with bpy.data.libraries.load(str(filepath), link=True) as (data_from, data_to):
        for attr in dir(data_to):
            setattr(data_to, attr, getattr(data_from, attr))
    # link object to scene collection
    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)

def update_tree_list():
    """Updates the list (cdbs_list) of displayed folders and files in the active directory."""

    bpy.context.scene.cdbs_list.clear()
    g_tree_elements.clear()
    check_folder = Path(CdbsEvn.g_library_path)
    logger('debug', f'Last clicked item: {PartsList.g_last_clicked_object}')
    if PartsList.g_last_clicked_object.is_dir():
        check_folder = PartsList.g_last_clicked_object
    current_position = PartsList.detect_current_position()
    if current_position == 'TREE':
        for object_path in check_folder.iterdir():
            if object_path.is_dir():
                g_tree_elements.append(object_path)
    elif current_position in {'COMPONENT', 'MODIFICATION'}:
        for object_path in check_folder.iterdir():
            if object_path.match('*/component') or object_path.match('*/modification'):
                logger('debug', translate('cdbs', 'Skip object:') + f' {object_path.name}')
                continue
            g_tree_elements.append(object_path)
    for idx, item in enumerate(g_tree_elements):
        rd = bpy.context.scene.cdbs_list.add()
        rd.name = item.name
        rd.path = str(item)
    # clear the previous index so as not to confuse users
    bpy.context.scene.cdbs_list_idx = 0

def open_tree_item():
    """Updates the path to reflect the selected folder and starts the list update function."""

    if not bpy.context.scene.cdbs_list_idx:
        bpy.context.scene.cdbs_list_idx = 0
    if not check_list_idx():
        update_tree_list()
        return
    path_item = Path(bpy.context.scene.cdbs_list[bpy.context.scene.cdbs_list_idx].path)
    if Path(path_item / CdbsEvn.g_program_name / 'modification').is_file():
        # switch to a set of files if the modification folder is selected for opening
        path_item = path_item / CdbsEvn.g_program_name
    if not path_item:
        logger('warning', translate('cdbs', 'Failed with get path:') + f' {bpy.context.scene.cdbs_list_idx}')
        return
    if not path_item.is_dir():
        logger('warning', translate('cdbs', 'The target path is not a directory.'))
        return
    PartsList.g_last_clicked_object = path_item
    update_tree_list()

def pull_objects():
    """Gets the current position and, if a target object is open, starts retrieving data for that object."""

    current_position = PartsList.detect_current_position()
    if current_position == 'ERROR':
        return
    PartsList.update_selected_object_uuid()
    if current_position == 'TREE':
        PartsList.update_components_list()
    elif current_position == 'COMPONENT':
        PartsList.update_component()
    elif current_position == 'MODIFICATION':
        PartsList.update_component_modificaion()
    else:
        logger('warning', translate('cdbs', 'Failed to determine the type of the open object:' + f' {current_position}'))
        return
    update_tree_list()
