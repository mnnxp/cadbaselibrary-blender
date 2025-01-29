from pathlib import Path
from bpy.types import Operator
from bpy.props import StringProperty
from . import CdbsEvn as CdbsEvn
from . import BtnUtil as BtnUtil
from . import PartsList as PartsList
from .CdbsStorage import CdbsStorage
from .Translate import translate
from .Logger import logger


class CDBS_OT_UploadUI(Operator):
    bl_idname = "cdbs.uploadui"
    bl_label = "CADBase Library Upload files"

    # Operator user properties, should be assigned using a single colon :
    # instead of using an equal sign = in Blender 2.8
    commit_msg: StringProperty(name = "", default = "")

    def __init__(self):
        self.uploading = False
        self.commit_msg = ''
        PartsList.update_selected_object_uuid()
        arg = (
            PartsList.g_selected_modification_uuid,
            PartsList.g_last_clicked_object,
            CdbsEvn.g_skip_blake3,
            CdbsEvn.g_force_upload
            )
        self.files = CdbsStorage(arg)
        self.cdbs_upload_list = self.files.processing_manager() or []
        if self.cdbs_upload_list:
            self.status_message = translate('cdbs', 'Change information:')
        else:
            self.status_message = translate('cdbs', 'Change information: no changes were found.')

    @classmethod # Will never run when poll returns false
    def poll(cls, context):
        return context.object

    def invoke(self, context, event): # Used for user interaction
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context): # Draw options (typically displayed in the tool-bar)
        layout = self.layout
        if self.uploading:
            layout.label(text="Uploading files to cloud storage (this can take a long time).")
            return

        ba_box = layout.box()
        ba_box.label(text="Commit message")
        ba_box.label(text="Is usually a brief description of the changes.")
        ba_box.prop(self, "commit_msg")

        layout.label(text=self.status_message)
        if not self.cdbs_upload_list:
            return
        fl_box = layout.box()
        fl_box_r1 = fl_box.row()
        fl_box_r1_c1 = fl_box_r1.column()
        fl_box_r1_c1.alignment = "LEFT"
        fl_box_r1_c1.label(text="№")
        fl_box_r1_c2 = fl_box_r1.column()
        fl_box_r1_c2.alignment = "CENTER"
        fl_box_r1_c2.label(text="Filename")
        fl_box_r1_c3 = fl_box_r1.column()
        fl_box_r1_c3.alignment = "RIGHT"
        fl_box_r1_c3.label(text="Status")
        for idx, (item, status) in enumerate(self.cdbs_upload_list):
            fl_box_ri = fl_box.row()
            fl_box_ri_c1 = fl_box_ri.column()
            fl_box_ri_c1.alignment = "LEFT"
            fl_box_ri_c1.label(text=str(idx+1))
            fl_box_ri_c2 = fl_box_ri.column()
            fl_box_ri_c2.alignment = "CENTER"
            fl_box_ri_c2.label(text=item)
            fl_box_ri_c3 = fl_box_ri.column()
            fl_box_ri_c3.alignment = "RIGHT"
            fl_box_ri_c3.label(text=status)
        layout.label(text="Please note: the changes indicated in the table")
        layout.label(text="will be applied only after clicking the OK button.")

    def execute(self, context): # Runs by default
        self.uploading = True
        self.files.processing_update(self.commit_msg)
        # Display messages for the user their in the interface, if any
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {'FINISHED'}