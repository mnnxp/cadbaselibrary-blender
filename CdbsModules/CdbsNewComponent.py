from bpy.types import Operator
from bpy.props import StringProperty
from pathlib import Path
import CdbsModules.CdbsEvn as CdbsEvn
import CdbsModules.BtnUtil as BtnUtil
import CdbsModules.PartsList as PartsList
import CdbsModules.DataHandler as DataHandler
from CdbsModules.CdbsApi import CdbsApi
from CdbsModules.QueriesApi import QueriesApi
from CdbsModules.CdbsAuth import CdbsAuth
from CdbsModules.Translate import translate
from CdbsModules.Logger import logger


class CDBS_OT_NewComponent(Operator):
    bl_idname = "cdbs.newcomponent"
    bl_label = "Adding a new component on CADBase"
    bl_description = "Registers a new component (part) on CADBase platform"

    # Operator user properties, should be assigned using a single colon :
    # instead of using an equal sign = in Blender 2.8
    component_name: StringProperty(name = "", default = "")

    def __init__(self):
        self.component_name = ""
        self.component_uuid = ""

    @classmethod # Will never run when poll returns false
    def poll(cls, context):
        return context.object

    def invoke(self, context, event): # Used for user interaction
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context): # Draw options (typically displayed in the tool-bar)
        layout = self.layout

        lp_box = layout.box()
        lp_box.label(text="A new component with the specified name will be")
        lp_box.label(text="created and added to the list of bookmarks for")
        lp_box.label(text="the authorized user. After successful creation")
        lp_box.label(text="the list of favorite components will be updated.")
        lp_box.prop(self, "component_name")

    def execute(self, context):
        if self.component_name:
            component_description = 'Blender ♥'
            CdbsApi(
                QueriesApi.register_component(
                    self.component_name, component_description
                )
            )
            self.component_uuid = str(DataHandler.deep_parsing_gpl('registerComponent'))
            if len(self.component_uuid) == CdbsEvn.g_len_uuid:
                PartsList.g_last_clicked_object = Path(CdbsEvn.g_library_path)
                BtnUtil.pull_objects()
                logger('debug', translate('cdbs', 'The component was successfully created.'))
            logger('debug', f'UUID: {self.component_uuid}')
        else:
            logger(
                'info',
                translate('cdbs', 'It is not possible to create a component without a name.'),
            )
        # Display messages for the user their in the interface, if any
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {'FINISHED'}