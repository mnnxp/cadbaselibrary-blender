from pathlib import Path
from bpy.types import AddonPreferences
from bpy.props import StringProperty
from .CdbsEvn import g_base_package

# Address of the main server of CADBase platform.
# The duplicates `CdbsModules.CdbsEvn.g_cadbase_api`.
g_cadbase_api = 'https://api.cadbase.rs'

class CdbsPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = g_base_package

    library_path: StringProperty(
        name="Library path",
        subtype='DIR_PATH',
        default="",
        description="The specified directory will be store data",
    )
    base_api: StringProperty(
        name="API Point",
        default=g_cadbase_api,
        description="Specify server with CADBase platform",
    )
    username: StringProperty(
        name="Username",
        default="",
        description="Username on CADBase platform",
    )
    password: StringProperty(
        name="Password",
        default="",
        subtype='PASSWORD',
        description="CADBase platform user password",
    )
    api_key: StringProperty(
        name="Authorization token",
        default="",
        subtype='PASSWORD',
        description="CADBase platform authorization token is issued after successful authorization.",
    )

    def draw(self, context):

        layout = self.layout

        lp_box = layout.box()
        lp_box.label(text="The specified directory will be used to create a local library and store data.")
        lp_box.label(text="Be careful, data in this directory may be overwritten.")
        lp_box.prop(self, "library_path")

        ba_box = layout.box()
        ba_box.label(text="You can specify the server on which the CADBase platform.")
        ba_box.label(text="Specify the URL or IP address of the server to connect to.")
        layout_r1 = ba_box.row()
        layout_r1_c1 = layout_r1.column()
        layout_r1_c1.prop(self, "base_api")
        layout_r1_c2 = layout_r1.column()
        point_icon = 'UNPINNED'
        if self.base_api == g_cadbase_api:
            point_icon = 'PINNED'
        layout_r1_c2.operator("cdbs.resetpoint", text="", icon=point_icon)

        r_auth = layout.box()
        r_auth.label(text="Enter the login and password to create a new user and receive an authorization token.")
        r_auth.label(text="For an existing user, an attempt will be made to obtain an authorization token with the specified password.")
        r_auth.prop(self, "username")
        r_auth.prop(self, "password")
        r_auth.operator("cdbs.signup", icon="KEYINGSET")