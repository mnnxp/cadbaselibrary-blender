# SPDX-License-Identifier: GPL-2.0-or-later

bl_info = {
    "name": "CADBase Library",
    "author": "mnnxp",
    "blender": (3, 4, 1),
    "location": "3D View > Sidebar", # FIXME: ???
    "description": "Tool for save data to cloud CADBase",
    "doc_url": "{BLENDER_MANUAL_URL}/addons/mesh/cadbase_library.html",
    "support": 'OFFICIAL', # FIXME: ???
    "category": "Import-Export", # FIXME: ???
}


if "bpy" in locals():
    import importlib
    importlib.reload(ui)
    if "export" in locals():
        importlib.reload(export)
else:
    import math

    import bpy
    from bpy.types import PropertyGroup
    from bpy.props import (
        StringProperty,
        BoolProperty,
        FloatProperty,
        EnumProperty,
        PointerProperty,
    )

    from . import (
        ui,
        logger,
    )


class SceneProperties(PropertyGroup):
    use_alignxy_face_area: BoolProperty(
        name="Face Areas",
        description="Normalize normals proportional to face areas",
        default=False,
    )

    export_format: EnumProperty(
        name="Format",
        description="Format type to export to",
        items=(
            ('OBJ', "OBJ", ""),
            ('PLY', "PLY", ""),
            ('STL', "STL", ""),
            ('X3D', "X3D", ""),
        ),
        default='STL',
    )
    use_export_texture: BoolProperty(
        name="Copy Textures",
        description="Copy textures on export to the output path",
        default=False,
    )
    use_apply_scale: BoolProperty(
        name="Apply Scale",
        description="Apply scene scale setting on export",
        default=False,
    )
    use_data_layers: BoolProperty(
        name="Data Layers",
        description=(
            "Export normals, UVs, vertex colors and materials for formats that support it "
            "significantly increasing file size"
        ),
    )
    export_path: StringProperty(
        name="Export Directory",
        description="Path to directory where the files are created",
        default="//",
        maxlen=1024,
        subtype="DIR_PATH",
    )
    thickness_min: FloatProperty(
        name="Thickness",
        description="Minimum thickness",
        subtype='DISTANCE',
        default=0.001,  # 1mm
        min=0.0,
        max=10.0,
    )
    threshold_zero: FloatProperty(
        name="Threshold",
        description="Limit for checking zero area/length",
        default=0.0001,
        precision=5,
        min=0.0,
        max=0.2,
    )
    angle_distort: FloatProperty(
        name="Angle",
        description="Limit for checking distorted faces",
        subtype='ANGLE',
        default=math.radians(45.0),
        min=0.0,
        max=math.radians(180.0),
    )
    angle_sharp: FloatProperty(
        name="Angle",
        subtype='ANGLE',
        default=math.radians(160.0),
        min=0.0,
        max=math.radians(180.0),
    )
    angle_overhang: FloatProperty(
        name="Angle",
        subtype='ANGLE',
        default=math.radians(45.0),
        min=0.0,
        max=math.radians(90.0),
    )


classes = (
    SceneProperties,

    ui.VIEWCL_tree,
    ui.VIEWCL_export,

    # operators.MESH_OT_print3d_clean_thin,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.cadbase_library = PointerProperty(type=SceneProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.cadbase_library
