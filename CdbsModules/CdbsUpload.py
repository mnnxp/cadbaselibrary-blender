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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uploading = False
        self.commit_msg = ''
        PartsList.update_selected_object_uuid()
        arg = (
            PartsList.g_selected_modification_uuid,
            PartsList.g_last_clicked_object,
            CdbsEvn.g_skip_hash,
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
        return wm.invoke_props_dialog(self, width=900)

    def draw(self, context): # Draw options (typically displayed in the tool-bar)
        layout = self.layout
        if self.uploading:
            layout.label(text="Uploading files to cloud storage (this can take a long time).")
            return

        ba_box = layout.box()
        ba_box.label(text="Commit message")
        ba_box.label(text="Recommendation: Describe in a short sentence (~50 characters) why the change was made, or what changed.")
        ba_box.prop(self, "commit_msg")

        layout.label(text=self.status_message)
        if not self.cdbs_upload_list:
            return
        # display table of changes
        headers = [
            'Filename',
            'Size (local)',
            'Date modified',
            'Size (remote)',
            'Upload date',
            'Status'
            ]
        row = layout.row(align=True)
        row.label(text="№")
        for header in headers:
            row.label(text=header)
        for idx, rows in enumerate(self.cdbs_upload_list):
            row = layout.row(align=True)
            row.label(text=str(idx+1))
            for item in rows:
                row.label(text=str(item))
        layout.label(text='Please note: changes to the table will only take effect after you click the "OK" button.')

    def execute(self, context): # Runs by default
        self.uploading = True
        self.files.processing_update(self.commit_msg)
        # Display messages for the user their in the interface, if any
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {'FINISHED'}