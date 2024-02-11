# SPDX-License-Identifier: GPL-2.0-or-later

bl_info = {
    "name": "CADBase Library",
    "author": "mnnxp",
    "blender": (3, 4, 1),
    "location": "3D View > Sidebar",
    "description": "Tool for save data to cloud CADBase",
    "doc_url": "{BLENDER_MANUAL_URL}/addons/mesh/cadbase_library.html",
    "support": 'COMMUNITY',
    "category": "Import-Export",
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

classes = (
    ui.VIEWCL_tree,
    ui.VIEWCL_export,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # bpy.types.Scene.cadbase_library = PointerProperty(type=SceneProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.cadbase_library
