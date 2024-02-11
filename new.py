import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath('./cadbase_library/CdbsModules/DataHandler.py'))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from pathlib import Path
from PySide2 import QtWidgets
import bpy
from bpy.types import Panel, Operator, UIList, PropertyGroup
from bpy.props import IntProperty, StringProperty, CollectionProperty
import CdbsModules.DataHandler as DataHandler
# import CdbsModules.CdbsEvn as CdbsEvn
from CdbsModules.CdbsStorage import CdbsStorage
import CdbsModules.PartsList as PartsList
from CdbsModules.Translate import translate
from new2 import CADBaseSetting
from new3 import ListItem, TOOL_UL_List, TOOL_OT_List_Add, TOOL_OT_List_Remove, TOOL_OT_List_Reorder


# g_selected_component_uuid: str = ''
# g_selected_modification_uuid: str = ''
g_last_clicked_object: Path = Path('')
class TreeEl():
    "Stores name and place pairs"
    def __init__(self, component_uuid, modification_uuid):
        self.component_uuid: str = component_uuid
        self.modification_uuid: str = modification_uuid
g_tree_elements = []

class EventMessage(Operator):
    bl_idname = "cdbs.cdbseventlog"
    bl_label = "CADBase Addon Event Log"

    idx : bpy.props.IntProperty(default=0)

    def execute(self, contect):
        self.report({'INFO'}, "part: {}, mod: {}".format(
            g_tree_elements[0].component_uuid,
            g_tree_elements[0].modification_uuid))
        # DataHandler.logger('warning', translate('CdbsAuth', g_selected_component_uuid))
        # DataHandler.logger('warning', translate('CdbsAuth', g_selected_modification_uuid))
        # DataHandler.logger('warning', translate('CdbsAuth', g_last_clicked_object))
        return {'FINISHED'}

class CdbsGetFavComponents(Operator):
    bl_idname = "cdbs.cdbsgetfavcomponents"
    bl_label = "CADBase Submit Changes"

    def execute(self, contect):
        PartsList.update_components_list()
        return {'FINISHED'}

class CdbsSubmitChanges(Operator):
    bl_idname = "cdbs.cdbssubmitchanges"
    bl_label = "CADBase Submit Changes"

    def execute(self, contect):
        arg = (
            PartsList.g_selected_modification_uuid,
            PartsList.g_last_clicked_object)
        CdbsStorage(arg)
        return {'FINISHED'}

class CdbsSettings(Operator):
    bl_idname = "cdbs.cdbssettings"
    bl_label = "CADBase Addon Settings"

    def execute(self, contect):
        client = CADBaseSetting()
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
        # global g_selected_component_uuid
        # global g_selected_modification_uuid
        # global g_last_clicked_object
        # global g_tree_elements
        layout = self.layout

        # The list is attached to an object.  Each object can have its own
        # Unique list; so the logic of the panel is to use the list associated
        # with the active object.
        scene = context.scene

        # Since we're in the View3d UI it might be useful to remind the user
        # what object they're currently interacting with.
        row = self.layout.row()
        # row.alignment = "CENTER"
        # row.label(text=object.name)
        row.label(text="Tree")

        # There are two rows.  The first row contains two columns.
        # The column on the left has the actual template_list.
        # The column on the right has the controls for editing
        # the list as a list.
        row = self.layout.row()
        row.alignment = "CENTER"

        if scene:
            # The left column, containing the list.
            col = row.column(align=True)
            col.template_list("TOOL_UL_List", "The_List", scene,
                              "demo_list", scene, "list_index")

            # The right column, containing the controls.
            # col = row.column(align=True)

            # col.operator("tool.list_add", text="", icon="ADD")
            # col.operator("tool.list_remove", text="", icon="REMOVE")

            # Only display the movement controls if the list is long enough
            # to justify movement
            if len(scene.demo_list) > 1:
                col.operator("tool.list_reorder", text="",
                    icon="TRIA_UP").direction = "UP"
                col.operator("tool.list_reorder", text="",
                    icon="TRIA_DOWN").direction = "DOWN"


            # The second row, containing the individual fields of the
            # list item so that they can be edited.  A row works for
            # the case of two small items but a more complex layout will
            # be necessary for more sophisticated list items.
            #
            # Shape Keys provides an example where a column is a better
            # choice than a row and the column's layout depends on the
            # position of the active item on the list.
            #
            # Shape Keys also provides an example of editing in the template
            # list.  That's not covered in this file.
            # row = self.layout.row()
            # if scene.list_index >= 0 and scene.demo_list:
            #     item = scene.demo_list[scene.list_index]

            #     row = self.layout.row()
            #     row.prop(item, "name")
            #     row.prop(item, "prop2")

            # list_parts = [
            #     "bvrebe hren tam hren tam (sdvl, rg,3gkm2)",
            #     "svbrbren hren tam hren tam (yhj76 5g34g)",
            #     "dsvuud hren tam hren tam (f3342332r 43g43g)",
            #     "yirnd_end hren tam hren tam (eewf3223g23g)"]
        # for idx, item in enumerate(list_parts):
        #     rd = context.scene.demo_list.set()
        #     rd.name = item
        #     rd.prop2 = idx
        # for idx, item in enumerate(list_parts):
        #     row_tree = tree_box.row()
        #     g_tree_elements.append(TreeEl(
        #         'hren tama {}'.format(idx),
        #         'set: {} -> '.format(item)))
        #     row_tree.operator("cdbs.cdbseventlog", text=item)

        # row_preview = layout.row()
        # row_preview.label(text="Preview")

        # row_up_parts_list.type_msg = "WARNING"
        # row_up_parts_list.text_msg = "WARNING HERE"
        row_options = layout.row()
        row_options.label(text="Options")
        row_up_parts_list = layout.operator("cdbs.cdbsgetfavcomponents", text = "Update components")
        row_push_files = layout.operator("cdbs.cdbssubmitchanges", text = "Upload files")
        # row_settings = layout.operator("cdbs.cdbseventlog", text = "Settings")
        row_settings = layout.operator("cdbs.cdbssettings", text = "Settings")

classes = [
    ViewCadbaseLibraryPanel,
    EventMessage,
    CdbsSettings,
    CdbsGetFavComponents,
    CdbsSubmitChanges,
    ListItem,
    TOOL_UL_List,
    TOOL_OT_List_Add,
    TOOL_OT_List_Remove,
    TOOL_OT_List_Reorder,
]

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

if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)
    register()