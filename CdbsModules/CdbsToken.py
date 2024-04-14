from pathlib import Path
from bpy.props import StringProperty
from bpy.types import Operator
import CdbsModules.CdbsEvn as CdbsEvn
import CdbsModules.PartsList as PartsList
from CdbsModules.CdbsAuth import CdbsAuth
from CdbsModules.Translate import translate
from CdbsModules.Logger import logger


class CDBS_OT_TokenUI(Operator):
    bl_idname = "cdbs.tokenui"
    bl_label = "CADBase Library Authorization"

    cdbs_username: StringProperty(name = "", default = "")
    cdbs_password: StringProperty(name = "", default = "", subtype='PASSWORD')

    def __init__(self):
        self.cdbs_username = ""
        self.cdbs_password = ""

    @classmethod # Will never run when poll returns false
    def poll(cls, context):
        return context.object

    def invoke(self, context, event): # Used for user interaction
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context): # Draw options (typically displayed in the tool-bar)
        layout = self.layout

        lp_box = layout.box()
        lp_box.label(text="Authorization")
        lp_box.label(text="CADBase platform access token will be saved locally, after successful authorization.")
        lp_box.label(text="When the authorization token expires, you will need to request a new authorization token by re-entering your username and password.")
        lp_box.label(text="Username")
        row = lp_box.row()
        row.prop(self, "cdbs_username")
        row2 = lp_box.row()
        row2.label(text="Password")
        row3 = lp_box.row()
        row3.prop(self, "cdbs_password")

    def execute(self, context): # Runs by default
        if self.cdbs_username and self.cdbs_password:
            CdbsAuth(self.cdbs_username, self.cdbs_password)
            logger('info', translate('cdbs', 'Configuration updated.'))
        else:
            logger('info', translate('cdbs', 'No changes.'))
        # Display messages for the user their in the interface, if any
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {'FINISHED'}