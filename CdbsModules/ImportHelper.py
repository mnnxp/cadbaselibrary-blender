import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from pathlib import Path
import CdbsModules.CdbsEvn as CdbsEvn
import CdbsModules.PartsList as PartsList
from CdbsModules.Translate import translate
from CdbsModules.Logger import logger


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
        if self.directory != CdbsEvn.g_library_path:
            CdbsEvn.g_library_path = self.directory
            PartsList.g_last_clicked_object = Path(CdbsEvn.g_library_path)
            CdbsEvn.save()
            CdbsEvn.update_settings()
            logger('info', translate('CadbaseMacro', 'Directory updated'))
        # Display messages for the user their in the interface, if any
        while CdbsEvn.g_stack_event:
            event = CdbsEvn.g_stack_event.pop(0)
            self.report({event.level}, str(event.msg))
        return {"FINISHED"}