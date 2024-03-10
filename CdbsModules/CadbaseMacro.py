import sys
from pathlib import Path
from PySide2 import QtWidgets
import bpy
from bpy.types import Panel, Operator
import CdbsModules.CdbsEvn as CdbsEvn
import CdbsModules.PartsList as PartsList
import CdbsModules.BtnUtil as BtnUtil
# from CdbsModules.Translate import translate
from CdbsModules.CdbsSetting import CdbsSetting
from CdbsModules.ToolUiList import TOOL_UL_List


class UpTreeLevel(Operator):
    bl_idname = "cdbs.uptreelevel"
    bl_label = "Return to parent object"

    def execute(self, context):
        if PartsList.g_last_clicked_object == Path(CdbsEvn.g_library_path):
            return {'FINISHED'}
        PartsList.g_last_clicked_object = PartsList.g_last_clicked_object.parent
        BtnUtil.update_tree_list()
        return {'FINISHED'}

class LinkFile(Operator):
    bl_idname = "cdbs.linkfile"
    bl_label = "Link file"

    def execute(self, context):
        BtnUtil.link_file_objects()
        return {'FINISHED'}

class PullData(Operator):
    bl_idname = "cdbs.pulldata"
    bl_label = "Pull data"

    def execute(self, context):
        BtnUtil.pull_objects()
        return {'FINISHED'}

class OpenListItem(Operator):
    bl_idname = "cdbs.openlistitem"
    bl_label = "Open List Item"

    def execute(self, context):
        BtnUtil.open_tree_item()
        return {'FINISHED'}

class CdbsPushChanges(Operator):
    bl_idname = "cdbs.cdbspushchanges"
    bl_label = "Push changes"

    def execute(self, context):
        BtnUtil.push_files_of_fileset()
        return {'FINISHED'}

class CdbsSettings(Operator):
    bl_idname = "cdbs.cdbssettings"
    bl_label = "Settings"

    def execute(self, context):
        client = CdbsSetting()
        client.show()
        app.exec_()
        return {'FINISHED'}

class ViewCadbaseLibraryPanel(Panel):
    bl_label = "CADBase Library"
    bl_idname = "OBJECT_PT_CdbsLibrary"
    bl_category = "Import-Export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        # global PartsList.g_selected_component_uuid
        # global PartsList.g_selected_modification_uuid
        # global PartsList.g_last_clicked_object
        # global g_tree_elements
        layout = self.layout

        # The list is attached to an object.  Each object can have its own
        # Unique list; so the logic of the panel is to use the list associated
        # with the active object.
        scene = context.scene

        # Since we're in the CADBase Library UI it might be useful to remind the user
        # what object (component, modification, etc.) they're currently interacting with.
        row = layout.row()
        row.alignment = "CENTER"
        row.label(text=f"Tree {PartsList.g_current_position}")

        if scene:
            # The left column, containing the list.
            # col = row.column(align=True)
            layout.template_list("TOOL_UL_List", "The_List", scene,
                              "demo_list", scene, "list_index")

            layout.operator("cdbs.uptreelevel", icon="BACK", text="Back")
            layout.operator("cdbs.openlistitem", icon="FORWARD", text="Open")
            layout.operator("cdbs.pulldata", icon="FILE_REFRESH")
            # layout.operator("cdbs.pulldata", icon="IMPORT")
            layout.operator("cdbs.linkfile", icon="LINKED")
            layout.operator("cdbs.cdbspushchanges", icon="EXPORT")

        # row_preview = layout.row()
        # row_preview.label(text="Preview")

        # row_options = layout.row()
        # row_options.label(text="Options")
        layout.operator("cdbs.cdbssettings", icon="OPTIONS")


app = QtWidgets.QApplication.instance()
if not app:
    app = QtWidgets.QApplication(sys.argv)
# BtnUtil.update_tree_list()