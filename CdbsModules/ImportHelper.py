import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator
import CdbsModules.CdbsSetting as CdbsSetting


class CDBS_OT_SelectDirectory(Operator, ImportHelper):
    bl_idname = "cdbs.selectdirectory"
    bl_label = "Select"
    bl_description = "The selected directory will store data about components, modifications and file sets."

    directory: StringProperty()

    filter_glob: StringProperty(
        default="",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        CdbsSetting.g_temp_library_path = self.directory
        return {"FINISHED"}