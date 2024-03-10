from pathlib import Path
import bpy
from CdbsModules.CdbsStorage import CdbsStorage
import CdbsModules.DataHandler as DataHandler
import CdbsModules.CdbsEvn as CdbsEvn
import CdbsModules.PartsList as PartsList

g_tree_elements = []

def push_files_of_fileset():
    current_position = PartsList.detect_current_position()
    if not current_position == 'MODIFICATION':
        DataHandler.logger('warning', f"Need open modification, now: {current_position}")
        return
    PartsList.update_selected_object_uuid()
    arg = (
        PartsList.g_selected_modification_uuid,
        PartsList.g_last_clicked_object)
    CdbsStorage(arg)

def link_file_objects():
    filepath = Path(bpy.context.scene.demo_list[bpy.context.scene.list_index].path)
    if Path(bpy.data.filepath) == filepath:
        DataHandler.logger('warning', 'This file is already linked')
        return
    if not filepath.exists():
        DataHandler.logger('warning', f"Skip not file: {filepath.name}")
        return
    if not filepath.suffix == '.blend':
        DataHandler.logger('warning', f"Skip file: {filepath.name}")
        return
    # link all objects
    with bpy.data.libraries.load(str(filepath), link=False) as (data_from, data_to):
        for attr in dir(data_to):
            setattr(data_to, attr, getattr(data_from, attr))
# enter_editmode=False
    # link object to scene collection
    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)

def update_tree_list():
    bpy.context.scene.demo_list.clear()
    g_tree_elements.clear()
    check_folder = Path(CdbsEvn.g_library_path)
    DataHandler.logger('warning', f"g_last_clicked_object: {PartsList.g_last_clicked_object}")
    if PartsList.g_last_clicked_object.is_dir():
        DataHandler.logger('warning', f"check_folder before: {check_folder}")
        check_folder = PartsList.g_last_clicked_object
        DataHandler.logger('warning', f"check_folder after: {check_folder}")
    current_position = PartsList.detect_current_position()
    if current_position == 'TREE':
        for object_path in check_folder.iterdir():
            if object_path.is_dir():
                g_tree_elements.append(object_path)
    elif current_position in {'COMPONENT', 'MODIFICATION'}:
        for object_path in check_folder.iterdir():
            if object_path.match('*/component') or object_path.match('*/modification'):
                DataHandler.logger('warning', f"Skip object: {object_path.name}")
                continue
            g_tree_elements.append(object_path)
    for idx, item in enumerate(g_tree_elements):
        rd = bpy.context.scene.demo_list.add()
        rd.name = item.name
        rd.path = str(item)
    # clear the previous index so as not to confuse users
    bpy.context.scene.list_index = 0

def open_tree_item():
    if not bpy.context.scene.demo_list:
        DataHandler.logger('warning', f"Not found bpy.context.scene.demo_list")
        return
    if not bpy.context.scene.list_index or bpy.context.scene.list_index >= len(bpy.context.scene.demo_list):
        DataHandler.logger('warning', f"Not found list_index: {bpy.context.scene.list_index}")
        bpy.context.scene.list_index = 0
    parent_item = Path(bpy.context.scene.demo_list[bpy.context.scene.list_index].path)
    if not parent_item:
        DataHandler.logger('warning', f"Failed with get parent path: {bpy.context.scene.list_index}")
        return
    if not parent_item.is_dir():
        DataHandler.logger('warning', 'Target path is not dir')
        return
    PartsList.g_last_clicked_object = parent_item
    update_tree_list()

def pull_objects():
    current_position = PartsList.detect_current_position()
    PartsList.update_selected_object_uuid()
    if current_position == 'TREE':
        PartsList.update_components_list()
    elif current_position == 'COMPONENT':
        PartsList.update_component()
    elif current_position == 'MODIFICATION':
        PartsList.update_component_modificaion()
    else:
        DataHandler.logger('warning', f"Failed get tree position: {current_position}")
        return
    update_tree_list()
