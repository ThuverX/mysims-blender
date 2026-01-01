import bpy
from bpy.types import ShaderNodeTree, NodeGroupOutput, NodeGroupInput, Material
from ..Props.MaterialProps import MySimsSingleMaterialProps
from ..MySimsFileSystem import MS_FILE_SYSTEM
from ..Serializers.ResourceKey import ResourceKey

SHADER_LAMBERT_NAME = "ms/k Lambert Shader"
SHADER_LAMBERT_TYPE = "0x94773578"


def create_shader_lambert():
    group_name = SHADER_LAMBERT_NAME
    if group_name in bpy.data.node_groups:
        return None
    lambert_group: ShaderNodeTree = bpy.data.node_groups.new(group_name, 'ShaderNodeTree')

    nodes = lambert_group.nodes
    links = lambert_group.links
    diffuse_shader = nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_shader.location = (100, 0)

    tint_node = nodes.new("ShaderNodeMixRGB")
    tint_node.location = (-100, 0)
    tint_node.blend_type = 'MULTIPLY'
    tint_node.inputs['Fac'].default_value = 1.0

    output_node: NodeGroupOutput = nodes.new("NodeGroupOutput")
    output_node.location = (300, 0)
    input_node: NodeGroupInput = nodes.new("NodeGroupInput")
    input_node.location = (-300, 0)

    lambert_group.interface.new_socket(name="diffuseMap", in_out='INPUT', socket_type='NodeSocketColor',
                                       description="Diffuse Texture")
    lambert_group.interface.new_socket(name="diffuseColor", in_out='INPUT', socket_type='NodeSocketColor',
                                       description="Diffuse Color")
    lambert_group.interface.new_socket(name="Shader", in_out='OUTPUT', socket_type='NodeSocketShader')

    links.new(input_node.outputs["diffuseMap"], tint_node.inputs["Color1"])
    links.new(input_node.outputs["diffuseColor"], tint_node.inputs["Color2"])
    links.new(tint_node.outputs["Color"], diffuse_shader.inputs["Color"])
    links.new(output_node.inputs["Shader"], diffuse_shader.outputs["BSDF"])

    return lambert_group


def create_material_lambert(material: Material, props: MySimsSingleMaterialProps):
    diffuse_texture = None
    alpha_texture = None
    diffuse_color = None

    for param in props.params:
        if param.type == "color" and param.name == "0x7FEE2D1A":
            diffuse_color = param.color
        if param.type == "map":
            path = MS_FILE_SYSTEM.get(ResourceKey.from_file_name(param.map.key))
            if path:
                if param.name == "0x6CC0FD85":  # Diffuse Map
                    diffuse_texture = path
                elif param.name == "0x2A20E51B" or param.name == "0x05D22FD3" or param.name == "0xC3FAAC4F":  # Alpha Map
                    alpha_texture = path

    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    nodes.clear()

    group_node = nodes.new("ShaderNodeGroup")
    group_node.node_tree = bpy.data.node_groups[SHADER_LAMBERT_NAME]
    group_node.location = (0, 0)

    material_output = nodes.new("ShaderNodeOutputMaterial")
    material_output.location = (300, 0)

    links.new(group_node.outputs[0], material_output.inputs[0])

    if diffuse_texture:
        texture_image = nodes.new(type="ShaderNodeTexImage")
        texture_image.image = bpy.data.images.load(diffuse_texture)
        texture_image.location = (-300, 200)

        links.new(texture_image.outputs["Color"], group_node.inputs["diffuseMap"])

    if diffuse_color:
        diffuse_color_node = nodes.new(type="ShaderNodeCombineColor")
        diffuse_color_node.mode = "RGB"
        diffuse_color_node.inputs["Red"].default_value = diffuse_color[0]
        diffuse_color_node.inputs["Green"].default_value = diffuse_color[1]
        diffuse_color_node.inputs["Blue"].default_value = diffuse_color[2]
        diffuse_color_node.location = (-300, -100)

        links.new(diffuse_color_node.outputs["Color"], group_node.inputs["diffuseColor"])

    return material
