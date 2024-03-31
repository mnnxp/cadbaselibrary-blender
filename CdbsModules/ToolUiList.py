from pathlib import Path
import bpy
from bpy.types import Panel, Operator, UIList, PropertyGroup
from bpy.props import IntProperty, StringProperty, CollectionProperty

#-----------------------------------------------------------------------------
#
# An extremely simple class that is used as the list item in the UIList.
# It is possible to use a builtin type instead but this allows customization.
# The content is fairly arbitrary, execpt that the member should be
# bpy.props (ToDo: Verify this.)
# Since it contains bpy.props, it must be registered.
class CdbsListItem(PropertyGroup):
    """Group of properties representing an item in the list."""

    name: StringProperty(
           name="Name",
           description="Name of folder or file in the local storage",
           default="Untitled")

    path: StringProperty(
           name="Path",
           description="Path to the selected object in local storage",
           default="")

#-----------------------------------------------------------------------------
#
# https://docs.blender.org/api/current/bpy.types.UIList.html#bpy.types.UIList
# The actual UIList class
# This class has a filter function that can be used to sort the properties
# into ascending or descending order using their name property.
class CDBS_UL_List(UIList):
    """Demo UIList."""
    bl_idname = "CDBS_UL_List"
    layout_type = "DEFAULT" # could be "COMPACT" or "GRID"
    # list_id ToDo

    # Custom properties, used in the filter functions
    # This property applies only if use_order_name is True.
    # In that case it determines whether to reverse the order of the sort.
    use_name_reverse: bpy.props.BoolProperty(
        name="Reverse Name",
        default=False,
        options=set(),
        description="Reverse name sort order",
    )

    # This properties tells whether to sort the list according to
    # the alphabetical order of the names.
    use_order_name: bpy.props.BoolProperty(
        name="Name",
        default=False,
        options=set(),
        description="Sort groups by their name (case-insensitive)",
    )

    # This property is the value for a simple name filter.
    filter_string: bpy.props.StringProperty(
        name="filter_string",
        default = "",
        description="Filter string for name"
    )

    # This property tells whether to invert the simple name filter
    filter_invert: bpy.props.BoolProperty(
        name="Invert",
        default = False,
        options=set(),
        description="Invert Filter"
    )

    #-------------------------------------------------------------------------
    # This function does two things, and as a result returns two arrays:
    # flt_flags - this is the filtering array returned by the filter
    #             part of the function. It has one element per item in the
    #             list and is set or cleared based on whether the item
    #             should be displayed.
    # flt_neworder - this is the sorting array returned by the sorting
    #             part of the function. It has one element per item
    #             the item is the new position in order for the
    #             item.
    # The arrays must be the same length as the list of items or empty
    def filter_items(self, context,
                    data, # Data from which to take Collection property
                    property # Identifier of property in data, for the collection
        ):


        items = getattr(data, property)
        if not len(items):
            return [], []

        # https://docs.blender.org/api/current/bpy.types.UI_UL_list.html
        # helper functions for handling UIList objects.
        if self.filter_string:
            flt_flags = bpy.types.UI_UL_list.filter_items_by_name(
                    self.filter_string,
                    self.bitflag_filter_item,
                    items,
                    propname="name",
                    reverse=self.filter_invert)
        else:
            flt_flags = [self.bitflag_filter_item] * len(items)

        # https://docs.blender.org/api/current/bpy.types.UI_UL_list.html
        # helper functions for handling UIList objects.
        if self.use_order_name:
            flt_neworder = bpy.types.UI_UL_list.sort_items_by_name(items, "name")
            if self.use_name_reverse:
                flt_neworder.reverse()
        else:
            flt_neworder = []


        return flt_flags, flt_neworder

    def draw_filter(self, context,
                    layout # Layout to draw the item
        ):

        row = layout.row(align=True)
        row.prop(self, "filter_string", text="Filter", icon="VIEWZOOM")
        row.prop(self, "filter_invert", text="", icon="ARROW_LEFTRIGHT")


        row.prop(self, "use_order_name", text="", icon='SORTSIZE')

    def draw_item(self, context,
                    layout, # Layout to draw the item
                    data, # Data from which to take Collection property
                    item, # Item of the collection property
                    icon, # Icon of the item in the collection
                    active_data, # Data from which to take property for the active element
                    active_propname, # Identifier of property in active_data, for the active element
                    index, # Index of the item in the collection - default 0
                    flt_flag # The filter-flag result for this item - default 0
            ):

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            set_icon = 'QUESTION'
            path = Path(item.path)
            if path.is_dir():
                set_icon = 'FILE_FOLDER'
            if path.is_file():
                if path.suffix == '.blend':
                    set_icon = 'FILE_BLEND'
                elif path.suffix == '.blend1':
                    set_icon = 'FILE_BACKUP'
                else:
                    set_icon = 'FILE_BLANK'
            layout.label(text=item.name, icon=set_icon)
            # layout.label(text=item.name)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")

#-----------------------------------------------------------------------------
#
# An extremely simple list reordering operator
# Replace context.scene.cdbs_list with the actual list
class CDBS_OT_List_Reorder(Operator):
    """ Add an Item to the UIList"""
    bl_idname = "cdbs.list_reorder"
    bl_label = "Add"
    bl_description = "add a new item to the list."

    direction: bpy.props.EnumProperty(items=(('UP', 'Up', ""),
                                              ('DOWN', 'Down', ""),))

    @classmethod
    def poll(cls, context):
        """ No reason to try to reorder a list with fewer than
            two items in it.
        """
        return (context.scene
                and context.scene.cdbs_list
                and len(context.scene.cdbs_list) > 1)

    def move_index(self):
        """ Move index of an item while clamping it. """
        index = bpy.context.scene.cdbs_list_idx
        list_length = len(bpy.context.scene.cdbs_list) - 1
        new_index = index + (-1 if self.direction == 'UP' else 1)

        bpy.context.scene.cdbs_list_idx = max(0, min(new_index, list_length))

    def execute(self, context):
        alist = context.scene.cdbs_list
        index = context.scene.cdbs_list_idx

        neighbor = index + (-1 if self.direction == 'UP' else 1)
        alist.move(neighbor, index)
        self.move_index()
        return {'FINISHED'}