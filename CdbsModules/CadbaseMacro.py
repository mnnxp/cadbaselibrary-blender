from pathlib import Path
import bpy
from bpy.types import Panel, Operator
from . import CdbsEvn as CdbsEvn
from .Logger import EventMessage  # is used in self.report
from . import PartsList as PartsList
from . import BtnUtil as BtnUtil
from . import CdbsNewUser as CdbsNewUser
from .ToolUiList import CDBS_UL_List
from .Logger import logger
from .Translate import translate


def invoke_operator_with_context(cdbs_operator):
    """Invokes a Blender operator, handling context differences based on Blender version."""
    try:
        if bpy.app.version < (4, 0, 0):
            cdbs_operator('INVOKE_DEFAULT')
        else:
            context_override = bpy.context.copy()
            with bpy.context.temp_override(**context_override):
                cdbs_operator('INVOKE_DEFAULT')
    except Exception as e:
        logger('error', str(e))
        logger(
            'error',
            translate(
                'cdbs',
                'The context is not selected correctly. \
Please try to select an object on the stage and open the modal window again.',
            ),
        )

class CDBS_OT_Click(Operator):
    bl_idname = "cdbs.click"
    bl_label = "Click Handler"
    bl_description = "Clicking on a folder will open it, \
while clicking on a file will attempt to load it and link it to the current collection in the scene"

    index: bpy.props.IntProperty()

    def execute(self, context):
        bpy.context.scene.cdbs_list_idx = self.index
        if Path(bpy.context.scene.cdbs_list[self.index].path).is_file():
            BtnUtil.link_file_objects()
        else:
            BtnUtil.open_tree_item()
            BtnUtil.update_tree_list()
        # Display messages for the user their in the interface
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {'FINISHED'}

class CDBS_OT_OpenDirectory(Operator):
    bl_idname = "cdbs.opendirectory"
    bl_label = "Open directory"
    bl_description = "Open the folder containing the selected file or directory in system's file explorer"

    index: bpy.props.IntProperty()

    def execute(self, context):
        BtnUtil.open_directory()
        # Display messages for the user their in the interface
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {'FINISHED'}

class CDBS_OT_CopyUrl(Operator):
    bl_idname = "cdbs.copyurl"
    bl_label = "Copy link"
    bl_description = "Copy the URL of the selected component to clipboard"

    def execute(self, context):
        BtnUtil.copy_component_url()
        # Display messages for the user their in the interface
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {'FINISHED'}

class CDBS_OT_OpenListItem(Operator):
    bl_idname = "cdbs.openlistitem"
    bl_label = "Open"
    bl_description = "Sets the selected folder as the current position and updates the list"

    def execute(self, context):
        BtnUtil.open_tree_item()
        BtnUtil.update_tree_list()
        # Request data if autpull is enabled and the opened folder is empty
        if CdbsEvn.g_autopull and not bpy.context.scene.cdbs_list:
            BtnUtil.pull_objects()
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
    bl_label = "Pull (data)"
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
        invoke_operator_with_context(bpy.ops.cdbs.newcomponent)
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
    bl_label = "Push (data)"
    bl_description = "Starts the process of sending changes from local to remote storage"

    def execute(self, context):
        current_position = PartsList.detect_current_position()
        if current_position == 'MODIFICATION':
            invoke_operator_with_context(bpy.ops.cdbs.uploadui)
        else:
            logger('warning', translate('cdbs', 'Need open modification, now:') + f' {current_position}')
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
        invoke_operator_with_context(bpy.ops.cdbs.settingui)
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
        invoke_operator_with_context(bpy.ops.cdbs.tokenui)
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

        # Navigation buttons (back and forward)
        row_nav = layout.row()
        row_nav.operator("cdbs.uptreelevel", icon="BACK")
        row_nav.operator("cdbs.openlistitem", icon="FORWARD")
        # File operations (pull and push)
        row_file = layout.row()
        row_file.operator("cdbs.pull", icon="FILE_REFRESH")
        row_file.operator("cdbs.push", icon="EXPORT")
        # Directory and URL actions
        row_dir = layout.row()
        row_dir.operator("cdbs.opendirectory", icon="DISK_DRIVE")
        row_dir.operator("cdbs.copyurl", icon="COPYDOWN")
        # File linkage and component registration
        row_actions = layout.row()
        row_actions.operator("cdbs.linkfile", icon="LINKED")
        row_actions.operator("cdbs.regcomponent", icon="ADD")
        # Options section
        layout.label(text="Options")
        row_options = layout.row()
        row_options.operator("cdbs.settings", icon="OPTIONS")
        row_options.operator("cdbs.authorization", icon="KEYINGSET")

        # Checks if the settings are updated. Updates the settings on first load
        # and when switching from the Add-on Manager after changing them there.
        cdbs_prefs = CdbsEvn.get_preferences()
        if cdbs_prefs:
            if (cdbs_prefs.library_path != CdbsEvn.g_library_path
                or cdbs_prefs.base_api != CdbsEvn.g_base_api):
                if not CdbsEvn.update_settings():
                    logger('debug', translate('cdbs', 'Failed to update preferences.'))
                PartsList.g_last_clicked_object = Path(CdbsEvn.g_library_path)