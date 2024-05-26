import sys
from pathlib import Path
import bpy
from bpy.types import Panel, Operator
import CdbsModules.CdbsEvn as CdbsEvn
from CdbsModules.Logger import EventMessage
import CdbsModules.PartsList as PartsList
import CdbsModules.BtnUtil as BtnUtil
import CdbsModules.CdbsNewUser as CdbsNewUser
from CdbsModules.ToolUiList import CDBS_UL_List


class CDBS_OT_OpenListItem(Operator):
    bl_idname = "cdbs.openlistitem"
    bl_label = "Open"
    bl_description = "Sets the selected folder as the current position and updates the list"

    def execute(self, context):
        BtnUtil.open_tree_item()
        # Display messages for the user their in the interface, if any
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {'FINISHED'}

class CDBS_OT_UpTreeLevel(Operator):
    bl_idname = "cdbs.uptreelevel"
    bl_label = "Go back"
    bl_description = "Sets the parent folder to active and updates the list"

    def execute(self, context):
        if PartsList.g_last_clicked_object == Path(CdbsEvn.g_library_path):
            return {'FINISHED'}
        if Path(PartsList.g_last_clicked_object / 'modification').is_file():
            # go up two levels if a folder with a set of files is open
            PartsList.g_last_clicked_object = PartsList.g_last_clicked_object.parent.parent
        else:
            PartsList.g_last_clicked_object = PartsList.g_last_clicked_object.parent
        BtnUtil.update_tree_list()
        # Display messages for the user their in the interface, if any
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {'FINISHED'}

class CDBS_OT_Pull(Operator):
    bl_idname = "cdbs.pull"
    bl_label = "Pull"
    bl_description = "Retrieves data from cloud storage and updates the list"

    def execute(self, context):
        BtnUtil.pull_objects()
        # Display messages for the user their in the interface, if any
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {'FINISHED'}

class CDBS_OT_RegComponent(Operator):
    bl_idname = "cdbs.regcomponent"
    bl_label = "Add component"
    bl_description = "Registers a new component (part) on CADBase platform"

    def execute(self, context):
        bpy.ops.cdbs.newcomponent('INVOKE_DEFAULT')
        # Display messages for the user their in the interface, if any
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {'FINISHED'}

class CDBS_OT_LinkFile(Operator):
    bl_idname = "cdbs.linkfile"
    bl_label = "Link file"
    bl_description = "Creates a reference to objects in the target file"

    def execute(self, context):
        BtnUtil.link_file_objects()
        # Display messages for the user their in the interface, if any
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {'FINISHED'}

class CDBS_OT_Push(Operator):
    bl_idname = "cdbs.push"
    bl_label = "Push"
    bl_description = "Starts the process of sending changes from local storage to the cloud."

    def execute(self, context):
        BtnUtil.push_files_of_fileset()
        # Display messages for the user their in the interface, if any
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {'FINISHED'}

class CDBS_OT_Settings(Operator):
    bl_idname = "cdbs.settings"
    bl_label = "Settings"
    bl_description = "Opens the tool (addon) settings in a separate window"

    def execute(self, context):
        bpy.ops.cdbs.settingui('INVOKE_DEFAULT')
        # Display messages for the user their in the interface, if any
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {'FINISHED'}

class CDBS_OT_Authorization(Operator):
    bl_idname = "cdbs.authorization"
    bl_label = "Authorization"
    bl_description = "Opens the window of authorization and updating the access token to CADBase platform"

    def execute(self, context):
        bpy.ops.cdbs.tokenui('INVOKE_DEFAULT')
        # Display messages for the user their in the interface, if any
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {'FINISHED'}

class CDBS_OT_SignUp(Operator):
    bl_idname = "cdbs.signup"
    bl_label = "Login"
    bl_description = "Sends requests to register and/or authorize the user"

    def execute(self, context):
        CdbsNewUser.register_new_user()
        # Display messages for the user their in the interface, if any
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {'FINISHED'}

class CDBS_PT_CadbaseLibrary(Panel):
    bl_label = "CADBase Library"
    bl_idname = "CDBS_PT_CadbaseLibrary"
    bl_category = "Import-Export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        # The list is attached to an object.  Each object can have its own
        # Unique list; so the logic of the panel is to use the list associated
        # with the active object.
        scene = context.scene

        # Since we're in the CADBase Library UI it might be useful to remind the user
        # what object (component, modification, etc.) they're currently interacting with.
        row = layout.row()
        row.alignment = "CENTER"
        row.label(text=f"{PartsList.g_current_position}")

        if not scene:
            return

        layout.template_list("CDBS_UL_List", "Cdbs_List", scene,
                            "cdbs_list", scene, "cdbs_list_idx")

        layout.operator("cdbs.openlistitem", icon="FORWARD")
        layout.operator("cdbs.uptreelevel", icon="BACK")
        layout.operator("cdbs.pull", icon="FILE_REFRESH")
        layout.operator("cdbs.regcomponent", icon="ADD")
        layout.operator("cdbs.linkfile", icon="LINKED")
        layout.operator("cdbs.push", icon="EXPORT")

        row_options = layout.row()
        row_options.label(text="Options")
        layout.operator("cdbs.settings", icon="OPTIONS")
        layout.operator("cdbs.authorization", icon="KEYINGSET")

        # Checks if the settings are updated. Updates the settings on first load
        # and when switching from the Add-on Manager after changing them there.
        cdbs_prefs = CdbsEvn.get_preferences()
        if cdbs_prefs:
            if (cdbs_prefs.library_path != CdbsEvn.g_library_path
                or cdbs_prefs.base_api != CdbsEvn.g_base_api):
                CdbsEvn.update_settings()
                PartsList.g_last_clicked_object = Path(CdbsEvn.g_library_path)