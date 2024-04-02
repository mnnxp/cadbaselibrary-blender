# SPDX-License-Identifier: GPL-2.0-or-later

bl_info = {
    "name": "CADBase Library",
    "author": "mnnxp",
    "version": (0, 0, 1),
    "blender": (3, 4, 1),
    "location": "3D View > Sidebar",
    "description": "This tool (addon) for synchronizing data local library with CADBase cloud storage.",
    "doc_url": "{BLENDER_MANUAL_URL}/addons/import_export/cadbase_library.html",
    "warning": "To update files in CADBase, Blake3 must be installed.",
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
    CDBS_PT_CadbaseLibrary,
    CDBS_OT_OpenListItem,
    CDBS_OT_UpTreeLevel,
    CDBS_OT_PullData,
    CDBS_OT_LinkFile,
    CDBS_OT_PushChanges,
    CDBS_OT_Settings,
    CDBS_OT_Authorization,
)
import CdbsModules.BtnUtil as BtnUtil
from CdbsModules.ToolUiList import CdbsListItem, CDBS_UL_List, CDBS_OT_List_Reorder
from CdbsModules.Translate import translations_dict

classes = (
    CDBS_PT_CadbaseLibrary,
    CDBS_OT_OpenListItem,
    CDBS_OT_UpTreeLevel,
    CDBS_OT_PullData,
    CDBS_OT_LinkFile,
    CDBS_OT_PushChanges,
    CDBS_OT_Settings,
    CDBS_OT_Authorization,
    CdbsListItem,
    CDBS_UL_List,
    CDBS_OT_List_Reorder,
)

def register():
    bpy.app.translations.register(__name__, translations_dict)
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.cdbs_list = CollectionProperty(type = CdbsListItem)
    bpy.types.Scene.cdbs_list_idx = IntProperty(name = "Index for cdbs_list",
                                             default = 0)

def unregister():
    del bpy.types.Scene.cdbs_list
    del bpy.types.Scene.cdbs_list_idx
    for c in classes:
        bpy.utils.unregister_class(c)
    bpy.app.translations.unregister(__name__)
