from bpy.types import Panel

from ..Serializers.MySimsMaterial import get_param_name
from ..Props.KeyProp import DrawKeyProperty
from ..Props.ObjectProps import MySimsObjectProps
from ..Props.MaterialProps import MySimsMaterialProps
from ..Operators.CopyMySimsMaterial import CopyMySimsMaterial
from ..Operators.EnableMySimsMaterial import EnableMySimsMaterial


class MySimsPanelMaterial(Panel):
    bl_label = "Material Settings"
    bl_idname = "OBJECT_PT_mysims_material"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MySims"

    def draw(self, context):
        layout = self.layout
        object = context.object

        if object is None:
            return

        if object.type != 'MESH' and object.type != 'EMPTY':
            return

        object_props: MySimsObjectProps = object.mysims_data
        material_props: MySimsMaterialProps = object.mysims_data.material

        if object_props.object_type == 'drawable':
            DrawKeyProperty(material_props, "set_key", layout, display_name="Material Set Key")

            layout.label(text="Materials:")
            layout.template_list(
                "MATERIAL_UL_list",
                "",
                material_props, "materials",
                material_props, "selected_material"
            )
            layout.separator()

            if material_props.selected_material is not None and len(material_props.materials) > 0:
                item = material_props.materials[material_props.selected_material]

                if item.locked:
                    layout.box().label(text="Please make a copy of this material to edit it", icon="INFO")

                row = layout.row()

                op_enable = row.operator(EnableMySimsMaterial.bl_idname, text="Preview", icon="HIDE_OFF")
                op_enable.index = -1
                op_copy = row.operator(CopyMySimsMaterial.bl_idname, text="Copy", icon="DUPLICATE")
                op_copy.index = -1

                box = layout.box()
                if item.locked:
                    box.enabled = False

                DrawKeyProperty(item, "key", box, only_errors=True, show_creation=True)

                parent_message = ""
                if item.key.state == "GOOD":
                    parent_message = "A copy of this material set will be created and exported"

                DrawKeyProperty(item, "parent", box, only_errors=True, show_creation=True, display_name="Parent",
                                custom_error=parent_message)

                box.prop(item, "shader_type")

                box.separator()
                box.label(text="Parameters:")
                box.template_list(
                    "MATERIAL_UL_param_list",
                    "",
                    item, "params",
                    item, "selected_param"
                )

                if item.selected_param is not None:
                    param = item.params[item.selected_param]
                    param_box = box.box()

                    row = param_box.row()
                    row.prop(param, "name")
                    row.label(text=f"({get_param_name(param.name)})")

                    if param.type == "color":
                        param_box.prop(param, "color")
                    elif param.type == "integer":
                        param_box.prop(param, "integer", text="Value")
                    elif param.type == "map":
                        DrawKeyProperty(param, "map", param_box)
