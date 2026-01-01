from bpy.types import Operator
from bpy.props import IntProperty

from ..Shaders.ShaderNodes import create_material
from ..Props.MaterialProps import MySimsMaterialProps


class EnableMySimsMaterial(Operator):
    bl_idname = "mysims.enable_material"
    bl_label = "Enable a mysims material"

    index: IntProperty(default=-1)

    def execute(self, context):
        obj = context.object
        material_props: MySimsMaterialProps = obj.mysims_data.material

        index = self.index

        if index == -1:
            index = material_props.selected_material
        else:
            material_props.selected_material = index

        create_material(obj, material_props.materials[index])

        return {'FINISHED'}
