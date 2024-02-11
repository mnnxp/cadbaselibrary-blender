# SPDX-License-Identifier: GPL-2.0-or-later

# Interface for this addon.


import bmesh
import bpy
from bpy.props import StringProperty, BoolProperty
from bpy.types import Panel, Operator
from PySide2 import QtWidgets, QtCore
from .logger import logger

class ViewCadbaseLibraryPanel:
    bl_category = "CADBase-Library"
    bl_space_type = 'VIEW_3D' # FIXME: ???
    bl_region_type = 'UI'

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH' and obj.mode in {'OBJECT', 'EDIT'}

class VIEWCL_tree(ViewCadbaseLibraryPanel, Panel):
    bl_idname = "cdbs.lib.ui"
    bl_label = "CADBase Library"

    #somewhere to remember the address of the file
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    def draw(self, context):
        layout = self.layout

        # TODO, make showing tree

        # cadbase_library = context.scene.cadbase_library

        # logger("error", "This does not work")

        # model = QFileSystemModel()
        # model.setRootPath(QDir.currentPath())
        # row = tree.setModel(model)

        # import bpy
        # print all objects
        # for obj in bpy.data.objects:
        #     logger("error", obj.name)
        # print all scene names in a list
        # logger("error", bpy.data.scenes.keys())

        # layout.label(text=bpy.data.filepath)
        # row = layout.row(align=True)

class VIEWCL_export(ViewCadbaseLibraryPanel, Panel):
    bl_label = "Export"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Expoooooort")
        row = layout.row(align=True)

        # TODO, make showing tree
        # layout = self.layout
        # layout.use_property_split = True
        # layout.use_property_decorate = False

        # cadbase_library = context.scene.cadbase_library

        # layout.prop(cadbase_library, "export_path", text="")
        # layout.prop(cadbase_library, "export_format")

        # col = layout.column()
        # col.prop(cadbase_library, "use_apply_scale")
        # col.prop(cadbase_library, "use_export_texture")
        # sub = col.column()
        # sub.active = cadbase_library.export_format != "STL"
        # sub.prop(cadbase_library, "use_data_layers")

        # layout.operator("mesh.cadbase_library", text="Export", icon='EXPORT')
