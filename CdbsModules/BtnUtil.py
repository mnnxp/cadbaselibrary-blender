from pathlib import Path
import bpy
from CdbsModules.CdbsStorage import CdbsStorage
import CdbsModules.CdbsEvn as CdbsEvn
import CdbsModules.PartsList as PartsList
from CdbsModules.Logger import logger

g_tree_elements = []

def check_list_idx():
    """Checks whether the leaf exists and whether the index is outside the array boundary."""

    if not bpy.context.scene.cdbs_list:
        logger('warning', f'Target list not found.')
        return False
    if bpy.context.scene.cdbs_list_idx >= len(bpy.context.scene.cdbs_list):
        logger('warning', f'Target index not found: {bpy.context.scene.cdbs_list_idx}')
        return False
    return True

def push_files_of_fileset():
    """Starts processing and sending files from the local file set to the cloud if a modification file set is open."""

    current_position = PartsList.detect_current_position()
    if not current_position == 'MODIFICATION':
        logger('warning', f"Need open modification, now: {current_position}")
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
        logger('warning', 'This file is already linked')
        return
    if not filepath.exists():
        logger('warning', f"Skip not file: {filepath.name}")
        return
    if not filepath.suffix == '.blend':
        logger('warning', f"Skip file: {filepath.name}")
        return
    # link all objects
    with bpy.data.libraries.load(str(filepath), link=False) as (data_from, data_to):
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
    logger('debug', f"g_last_clicked_object: {PartsList.g_last_clicked_object}")
    if PartsList.g_last_clicked_object.is_dir():
        logger('debug', f"check_folder before: {check_folder}")
        check_folder = PartsList.g_last_clicked_object
        logger('debug', f"check_folder after: {check_folder}")
    current_position = PartsList.detect_current_position()
    if current_position == 'TREE':
        for object_path in check_folder.iterdir():
            if object_path.is_dir():
                g_tree_elements.append(object_path)
    elif current_position in {'COMPONENT', 'MODIFICATION'}:
        for object_path in check_folder.iterdir():
            if object_path.match('*/component') or object_path.match('*/modification'):
                logger('debug', f"Skip object: {object_path.name}")
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
        return
    path_item = Path(bpy.context.scene.cdbs_list[bpy.context.scene.cdbs_list_idx].path)
    if Path(path_item / CdbsEvn.g_program_name / 'modification').is_file():
        # switch to a set of files if the modification folder is selected for opening
        path_item = path_item / CdbsEvn.g_program_name
    if not path_item:
        logger('warning', f"Failed with get path: {bpy.context.scene.cdbs_list_idx}")
        return
    if not path_item.is_dir():
        logger('warning', 'Target path is not dir')
        return
    PartsList.g_last_clicked_object = path_item
    update_tree_list()

def pull_objects():
    """Gets the current position and, if a target object is open, starts retrieving data for that object."""

    if len(CdbsEvn.g_library_path) < 2:
        logger('warning', f"Please specify path to the local library in the tool (addon) settings.")
        return
    current_position = PartsList.detect_current_position()
    PartsList.update_selected_object_uuid()
    if current_position == 'TREE':
        PartsList.update_components_list()
    elif current_position == 'COMPONENT':
        PartsList.update_component()
    elif current_position == 'MODIFICATION':
        PartsList.update_component_modificaion()
    else:
        logger('warning', f"Failed get tree position: {current_position}")
        return
    update_tree_list()
