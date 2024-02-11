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
class ListItem(PropertyGroup):
    """Group of properties representing an item in the list."""

    name: StringProperty(
           name="Name",
           description="A name for this item",
           default="Untitled")

    prop2: StringProperty(
           name="Any other property you want",
           description="",
           default="")

#-----------------------------------------------------------------------------
#
# https://docs.blender.org/api/current/bpy.types.UIList.html#bpy.types.UIList
# The actual UIList class
# This class has a filter function that can be used to sort the properties
# into ascending or descending order using their name property.
class TOOL_UL_List(UIList):
    """Demo UIList."""
    bl_idname = "TOOL_UL_List"
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


        row = layout.row(align=True)
        row.label(text="Order by:")
        row.prop(self, "use_order_name", toggle=True)

        icon = 'TRIA_UP' if self.use_name_reverse else 'TRIA_DOWN'
        row.prop(self, "use_name_reverse", text="", icon=icon)

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
            layout.label(text=item.name)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")

#-----------------------------------------------------------------------------
#
# An extremely simple list add operator
# Replace context.scene.demo_list with the actual list
class TOOL_OT_List_Add(Operator):
    """ Add an Item to the UIList"""
    bl_idname = "tool.list_add"
    bl_label = "Add"
    bl_description = "add a new item to the list."

    @classmethod
    def poll(cls, context):
        """ We can only add items to the list of an active object
            but the list may be empty or doesn't yet exist so
            just this function can only check if there is an active object
        """
        return context.scene

    def execute(self, context):
        context.scene.demo_list.add()
        return {'FINISHED'}

#-----------------------------------------------------------------------------
#
# An extremely simple list remove operator
# Replace context.scene.demo_list with the actual list
# It's only possible to remove the item that is indexed
# The reorder routine keeps track of the index.
class TOOL_OT_List_Remove(Operator):
    """ Add an Item to the UIList"""
    bl_idname = "tool.list_remove"
    bl_label = "Add"
    bl_description = "Remove an new item from the list."

    @classmethod
    def poll(cls, context):
        """ We can only remove items from the list of an active object
            that has items in it, but the list may be empty or doesn't
            yet exist and there's no reason to remove an item from an empty
            list.
        """
        return (context.scene
                and context.scene.demo_list
                and len(context.scene.demo_list))

    def execute(self, context):
        alist = context.scene.demo_list
        index = context.scene.list_index
        context.scene.demo_list.remove(index)
        context.scene.list_index = min(max(0, index - 1), len(alist) - 1)
        return {'FINISHED'}

#-----------------------------------------------------------------------------
#
# An extremely simple list reordering operator
# Replace context.scene.demo_list with the actual list
class TOOL_OT_List_Reorder(Operator):
    """ Add an Item to the UIList"""
    bl_idname = "tool.list_reorder"
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
                and context.scene.demo_list
                and len(context.scene.demo_list) > 1)

    def move_index(self):
        """ Move index of an item while clamping it. """
        index = bpy.context.scene.list_index
        list_length = len(bpy.context.scene.demo_list) - 1
        new_index = index + (-1 if self.direction == 'UP' else 1)

        bpy.context.scene.list_index = max(0, min(new_index, list_length))

    def execute(self, context):
        alist = context.scene.demo_list
        index = context.scene.list_index

        neighbor = index + (-1 if self.direction == 'UP' else 1)
        alist.move(neighbor, index)
        self.move_index()
        return {'FINISHED'}