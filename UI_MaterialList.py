import bpy
from .Operators_CopyMySimsMaterial import CopyMySimsMaterial
from .Operators_EnableMySimsMaterial import EnableMySimsMaterial

class MATERIAL_UL_list(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row()
        if item.key.state == "GOOD":
            row.label(text=item.key.key, icon="DECORATE")
        else:
            row.label(text=item.key.key, icon="MATERIAL")

        if item.key.key == "":
            row.label(text="(Missing key)")

        icons = row.row(align=True)
        enable_op = icons.operator(EnableMySimsMaterial.bl_idname, text="", icon="HIDE_OFF")
        enable_op.index = index
        icons.operator(CopyMySimsMaterial.bl_idname, text="", icon="DUPLICATE")
