# SPDX-License-Identifier: GPL-2.0-or-later

bl_info = {
    "name": "CADBase Library",
    "author": "mnnxp",
    "blender": (3, 4, 1),
    "location": "3D View > Sidebar",
    "description": "Tool for save data to cloud CADBase",
    "doc_url": "{BLENDER_MANUAL_URL}/addons/import_export/cadbase_library.html",
    "support": 'COMMUNITY',
    "category": "Import-Export",
}


import os, sys
from pathlib import Path

SCRIPT_DIR = os.path.abspath(str(Path(__file__).parent / 'CdbsModules'))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import bpy
from bpy.props import IntProperty, CollectionProperty
from CdbsModules.CadbaseMacro import (
    ViewCadbaseLibraryPanel,
    CdbsSettings,
    CdbsPushChanges,
    UpTreeLevel,
    LinkFile,
    PullData,
    OpenListItem,
)
import CdbsModules.BtnUtil as BtnUtil
from CdbsModules.ToolUiList import ListItem, TOOL_UL_List, TOOL_OT_List_Reorder

classes = (
    ViewCadbaseLibraryPanel,
    CdbsSettings,
    CdbsPushChanges,
    UpTreeLevel,
    LinkFile,
    PullData,
    OpenListItem,
    ListItem,
    TOOL_UL_List,
    TOOL_OT_List_Reorder,
)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.demo_list = CollectionProperty(type = ListItem)
    bpy.types.Scene.list_index = IntProperty(name = "Index for demo_list",
                                             default = 0)

def unregister():
    del bpy.types.Scene.demo_list
    del bpy.types.Scene.list_index
    for c in classes:
        bpy.utils.unregister_class(c)
