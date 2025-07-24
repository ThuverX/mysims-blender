import bpy

from .Serializers_MySimsMaterial import get_param_name


class MATERIAL_UL_param_list(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.33)

        name = get_param_name(item.name)

        if item.type == "color":
            split.label(text=name, icon="COLOR")
        elif item.type == "map":
            split.label(text=name, icon="IMAGE_DATA")
        else:
            split.label(text=name, icon="PROPERTIES")

        if name != item.name:
            split.label(text=f"({item.name})")
        else:
            split.label(text="")

        split.alignment = "RIGHT"
        if item.type == "color":
            split.label(text="Color")
        elif item.type == "map":
            split.label(text="Image")
        else:
            split.label(text="Value")

