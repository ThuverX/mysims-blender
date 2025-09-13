import bpy
from bpy.types import ShaderNodeTree, NodeGroupOutput, NodeGroupInput, Material
from .Props_MaterialProps import MySimsSingleMaterialProps
from .MySimsFileSystem import MS_FILE_SYSTEM
from .Serializers_ResourceKey import ResourceKey

SHADER_TERRAIN_LIGHT_MAP_TINTED_NAME = "ms/k Terrain Light Map Tinted Shader"
SHADER_TERRAIN_LIGHT_MAP_TINTED_TYPE = "0x224E7FEE"


def create_shader_terrain_light_map_tinted():
    group_name = SHADER_TERRAIN_LIGHT_MAP_TINTED_NAME
    if group_name in bpy.data.node_groups:
        return None
    group_node: ShaderNodeTree = bpy.data.node_groups.new(group_name, 'ShaderNodeTree')

    nodes = group_node.nodes
    links = group_node.links
    diffuse_shader = nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_shader.location = (100, 0)

    tint_node = nodes.new("ShaderNodeMixRGB")
    tint_node.location = (-100, 0)
    tint_node.blend_type = 'MULTIPLY'
    tint_node.inputs['Fac'].default_value = 1.0

    ambient_node = nodes.new("ShaderNodeMixRGB")
    ambient_node.location = (-100, 0)
    ambient_node.blend_type = 'MULTIPLY'
    ambient_node.inputs['Fac'].default_value = 1.0

    ambient_mul_node = nodes.new("ShaderNodeVectorMath")
    ambient_mul_node.location = (-100, 0)
    ambient_mul_node.operation = 'SCALE'
    ambient_mul_node.inputs[3].default_value = 2

    output_node: NodeGroupOutput = nodes.new("NodeGroupOutput")
    output_node.location = (300, 0)
    input_node: NodeGroupInput = nodes.new("NodeGroupInput")
    input_node.location = (-300, 0)

    group_node.interface.new_socket(name="diffuseMap", in_out='INPUT', socket_type='NodeSocketColor',
                                       description="Diffuse Texture")
    group_node.interface.new_socket(name="ambientMap", in_out='INPUT', socket_type='NodeSocketColor',
                                       description="Ambient Texture")
    group_node.interface.new_socket(name="diffuseColor", in_out='INPUT', socket_type='NodeSocketColor',
                                       description="Diffuse Color")
    group_node.interface.new_socket(name="Shader", in_out='OUTPUT', socket_type='NodeSocketShader')

    links.new(input_node.outputs["diffuseMap"], ambient_node.inputs["Color1"])
    links.new(input_node.outputs["ambientMap"], ambient_mul_node.inputs[0])

    links.new(ambient_mul_node.outputs["Vector"], ambient_node.inputs["Color2"])

    links.new(ambient_node.outputs["Color"], tint_node.inputs["Color1"])

    links.new(input_node.outputs["diffuseColor"], tint_node.inputs["Color2"])
    links.new(tint_node.outputs["Color"], diffuse_shader.inputs["Color"])
    links.new(output_node.inputs["Shader"], diffuse_shader.outputs["BSDF"])

    return group_node


def create_material_terrain_light_map_tinted(material: Material, props: MySimsSingleMaterialProps):
    diffuse_texture = None
    alpha_texture = None
    ambient_texture = None
    diffuse_color = None

    for param in props.params:
        if param.type == "color" and param.name == "0x7FEE2D1A":
            diffuse_color = param.color
        if param.type == "map":
            path = MS_FILE_SYSTEM.get(ResourceKey.from_file_name(param.map.key))
            if path:
                if param.name == "0x6CC0FD85":  # Diffuse Map
                    diffuse_texture = path
                elif param.name == "0x20CB22B7":
                    ambient_texture = path
                elif param.name == "0x2A20E51B" or param.name == "0x05D22FD3" or param.name == "0xC3FAAC4F":  # Alpha Map
                    alpha_texture = path

    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    nodes.clear()

    group_node = nodes.new("ShaderNodeGroup")
    group_node.node_tree = bpy.data.node_groups[SHADER_TERRAIN_LIGHT_MAP_TINTED_NAME]
    group_node.location = (0, 0)

    material_output = nodes.new("ShaderNodeOutputMaterial")
    material_output.location = (300, 0)

    links.new(group_node.outputs[0], material_output.inputs[0])

    if diffuse_texture:
        texture_image = nodes.new(type="ShaderNodeTexImage")
        texture_image.image = bpy.data.images.load(diffuse_texture)
        texture_image.location = (-300, 200)

        links.new(texture_image.outputs["Color"], group_node.inputs["diffuseMap"])

    if ambient_texture:
        uv2_node = nodes.new("ShaderNodeUVMap")
        uv2_node.uv_map = "uv1"

        ambient_image = nodes.new(type="ShaderNodeTexImage")
        ambient_image.image = bpy.data.images.load(ambient_texture)
        ambient_image.location = (-400, 200)
        links.new(uv2_node.outputs["UV"], ambient_image.inputs["Vector"])

        links.new(ambient_image.outputs["Color"], group_node.inputs["ambientMap"])

    if diffuse_color:
        diffuse_color_node = nodes.new(type="ShaderNodeCombineColor")
        diffuse_color_node.mode = "RGB"
        diffuse_color_node.inputs["Red"].default_value = diffuse_color[0]
        diffuse_color_node.inputs["Green"].default_value = diffuse_color[1]
        diffuse_color_node.inputs["Blue"].default_value = diffuse_color[2]
        diffuse_color_node.location = (-300, -100)

        links.new(diffuse_color_node.outputs["Color"], group_node.inputs["diffuseColor"])

    return material
