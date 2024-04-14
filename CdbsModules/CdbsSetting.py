import bpy
from bpy.types import Operator
from bpy.props import StringProperty
from pathlib import Path
import CdbsModules.CdbsEvn as CdbsEvn
import CdbsModules.PartsList as PartsList
from CdbsModules.CdbsAuth import CdbsAuth
from CdbsModules.Translate import translate
from CdbsModules.Logger import logger


class CDBS_OT_ResetPoint(Operator):
    bl_idname = "cdbs.resetpoint"
    bl_label = "Reset API point"
    bl_description = "Sets as value the API point of the main CADBase platform server"

    def execute(self, context):
        CdbsEvn.g_resetpoint_flag = True
        logger('debug', translate('CadbaseMacro', 'Need reset point'))
        return {'FINISHED'}

class CDBS_OT_SettingUI(Operator):
    bl_idname = "cdbs.settingui"
    bl_label = "CADBase Library Configuration"

    # Operator user properties, should be assigned using a single colon :
    # instead of using an equal sign = in Blender 2.8
    library_path: StringProperty(name = "", default = "")
    base_api: StringProperty(name = "", default = "")

    def __init__(self):
        if CdbsEvn.g_library_path:
            self.library_path = CdbsEvn.g_library_path
        if CdbsEvn.g_base_api:
            self.base_api = CdbsEvn.g_base_api

    @classmethod # Will never run when poll returns false
    def poll(cls, context):
        return context.object

    def invoke(self, context, event): # Used for user interaction
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context): # Draw options (typically displayed in the tool-bar)
        layout = self.layout

        if CdbsEvn.g_resetpoint_flag:
            self.base_api = CdbsEvn.g_cadbase_api
            CdbsEvn.g_resetpoint_flag = False
            logger('debug', translate('CadbaseMacro', 'Reset point finish'))

        lp_box = layout.box()
        lp_box.label(text="Library path")
        lp_box.label(text="The addon will use this directory to save downloaded files.")
        lp_box.label(text="Be careful, data in this directory may be overwritten.")
        lp_box.label(text="Changing the library path will require restarting Blender.")
        row = lp_box.row()
        col = row.column()
        col.prop(self, "library_path")
        col2 = row.column()
        col2.operator("cdbs.selectdirectory", text="", icon="FILE_FOLDER")

        ba_box = layout.box()
        ba_box.label(text="Point API")
        ba_box.label(text="Here you can specify the server on which the CADBase platform.")
        ba_box.label(text="Specify the server (URL or IP) \nif you need to connect to the unofficial CADBase platform server.")
        row = ba_box.row()
        col11 = row.column()
        col11.prop(self, "base_api")
        col12 = row.column()
        point_icon = 'UNPINNED'
        if self.base_api == CdbsEvn.g_cadbase_api:
            point_icon = 'PINNED'
        col12.operator("cdbs.resetpoint", text="", icon=point_icon)

    def execute(self, context): # Runs by default
        update_settings = False
        if self.base_api:
            CdbsEvn.g_base_api = self.base_api
            update_settings = True
        if self.library_path != CdbsEvn.g_library_path:
            CdbsEvn.g_library_path = self.library_path
            PartsList.g_last_clicked_object = Path(CdbsEvn.g_library_path)
            update_settings = True
        if update_settings:
            logger('info', translate('CadbaseMacro', 'Updating settings'))
            CdbsEvn.save()
            CdbsEvn.update_settings()
            logger('info', translate('CadbaseMacro', 'Configuration updated'))
        else:
            logger('info', translate('CadbaseMacro', 'No changes found'))
        # Display messages for the user their in the interface, if any
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {'FINISHED'}