# SPDX-License-Identifier: GPL-2.0-or-later

bl_info = {
    "name": "CADBase Library",
    "author": "mnnxp",
    "version": (0, 1, 4),
    "blender": (4, 2, 0),
    "location": "3D View > Sidebar",
    "description": "Add-on for synchronizing local data with cloud storage",
    "doc_url": "https://gitlab.com/cadbase/cadbaselibrary-blender/-/blob/master/README.md",
    "support": 'COMMUNITY',
    "category": "Import-Export",
}


import os, sys
from pathlib import Path

import bpy
from bpy.props import IntProperty, CollectionProperty
from .CdbsModules.CadbaseMacro import (
    CDBS_PT_CadbaseLibrary,
    CDBS_OT_OpenListItem,
    CDBS_OT_UpTreeLevel,
    CDBS_OT_Pull,
    CDBS_OT_RegComponent,
    CDBS_OT_LinkFile,
    CDBS_OT_Push,
    CDBS_OT_Settings,
    CDBS_OT_Authorization,
    CDBS_OT_SignUp,
)
from .CdbsModules.CdbsSetting import CDBS_OT_SettingUI, CDBS_OT_ResetPoint
from .CdbsModules.CdbsToken import CDBS_OT_TokenUI
from .CdbsModules.CdbsNewComponent import CDBS_OT_NewComponent
from .CdbsModules.ImportHelper import CDBS_OT_SelectDirectory
from .CdbsModules.ToolUiList import CdbsListItem, CDBS_UL_List
from .CdbsModules.Translate import translations_dict
from .CdbsModules import CdbsEvn as CdbsEvn

CdbsEvn.g_base_package = str(__package__)
from .CdbsModules.CdbsPreferences import CdbsPreferences


classes = (
    CDBS_PT_CadbaseLibrary,
    CDBS_OT_OpenListItem,
    CDBS_OT_UpTreeLevel,
    CDBS_OT_Pull,
    CDBS_OT_RegComponent,
    CDBS_OT_NewComponent,
    CDBS_OT_LinkFile,
    CDBS_OT_Push,
    CDBS_OT_Settings,
    CDBS_OT_SettingUI,
    CDBS_OT_ResetPoint,
    CDBS_OT_SelectDirectory,
    CDBS_OT_Authorization,
    CDBS_OT_SignUp,
    CDBS_OT_TokenUI,
    CdbsListItem,
    CDBS_UL_List,
    CdbsPreferences,
)

def register():
    bpy.app.translations.register(__package__, translations_dict)
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
    bpy.app.translations.unregister(__package__)
