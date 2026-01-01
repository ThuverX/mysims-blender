import bpy
from bpy.types import Object
from ..Props.MaterialProps import MySimsSingleMaterialProps
from .ShaderLambert import create_shader_lambert, create_material_lambert, SHADER_LAMBERT_TYPE
from .ShaderTerrainLightMapTinted import create_shader_terrain_light_map_tinted, create_material_terrain_light_map_tinted, SHADER_TERRAIN_LIGHT_MAP_TINTED_TYPE


def register_shaders():
    create_shader_lambert()
    create_shader_terrain_light_map_tinted()


def unregister_shaders():
    pass


def create_material(obj: Object, props: MySimsSingleMaterialProps):
    register_shaders()

    old = bpy.data.materials.get(str(props.key.key))
    if old:
        material = old
    else:
        material = bpy.data.materials.new(str(props.key.key))

    if props.shader_type == SHADER_LAMBERT_TYPE:
        create_material_lambert(material, props)
    elif props.shader_type == SHADER_TERRAIN_LIGHT_MAP_TINTED_TYPE:
        create_material_terrain_light_map_tinted(material, props)

    if material and obj.type == 'MESH':
        if len(obj.data.materials) == 0:
            obj.data.materials.append(material)
        else:
            obj.data.materials[0] = material

    return material

