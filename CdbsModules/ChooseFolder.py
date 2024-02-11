import bpy

# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
import os.path


class ChooseFolder(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "cdbs.choosefolder"
    bl_label = "Choose a folder for the library"

    # ExportHelper mixin class uses this
    filename_ext = "."
    use_filter_folder = True

    def execute(self, context):
        userpath = self.properties.filepath
        if not os.path.isdir(userpath):
            msg = "Please select a directory not a file\n" + userpath
            self.report({'WARNING'}, msg)

        #Insert the desired logic here to write to the directory.
        self.report({'INFO'}, "Vse norm")

        return{'FINISHED'}



# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    bpy.utils.register_class(ChooseFolder)


def unregister():
    bpy.utils.unregister_class(ChooseFolder)


# if __name__ == "__main__":
#     register()

#     # test call
#     bpy.ops.cdbs.choosefolder('INVOKE_DEFAULT')
