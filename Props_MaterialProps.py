from bpy.types import PropertyGroup
from bpy.props import StringProperty, EnumProperty, IntProperty, FloatVectorProperty, CollectionProperty, BoolProperty
from .MySimsShaders import get_shader_list_as_enum
from .Props_KeyProp import KeyProperty


class MySimsMaterialParam(PropertyGroup):
    name: StringProperty(name="Name")
    type: EnumProperty(name="Type", items=[
        ("color", "Color", ""),
        ("integer", "Integer", ""),
        ("map", "Map", "")
    ])
    color: FloatVectorProperty(name="Color", subtype="COLOR", size=4)
    map: KeyProperty(name="Map")
    integer: IntProperty(name="Integer")


def single_material_updated(self, context):
    obj = context.object
    materials_props: MySimsMaterialProps = obj.mysims_data.material
    if materials_props.selected_material is None:
        return
    material_props: MySimsSingleMaterialProps = materials_props.materials[materials_props.selected_material]


class MySimsSingleMaterialProps(PropertyGroup):
    shader_type: EnumProperty(name="Shader", update=single_material_updated, items=get_shader_list_as_enum())
    parent: KeyProperty(update=single_material_updated)
    key: KeyProperty(update=single_material_updated)
    params: CollectionProperty(name="Params", type=MySimsMaterialParam)
    selected_param: IntProperty(name="Index", update=single_material_updated, default=0)
    locked: BoolProperty(default=True)


class MySimsMaterialProps(PropertyGroup):
    set_key: KeyProperty(name="Material Set Key")
    materials: CollectionProperty(name="Materials", type=MySimsSingleMaterialProps)
    selected_material: IntProperty(name="Index", default=0)

