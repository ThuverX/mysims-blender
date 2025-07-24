import os
import bmesh

from .Shaders_ShaderNodes import create_material
from .Props_KeyProp import SetKeyProperty
from .Serializers_MySimsMaterial import MySimsMaterial, MySimsMaterialSet
from .Serializers_HavokPhysics import HavokPhysics
from .Serializers_Serializer import Serializer
from .Props_MaterialProps import MySimsMaterialProps, MySimsSingleMaterialProps
from .util import *
from .Serializers_ResourceKey import ResourceKey
from .MySimsFileSystem import MS_FILE_SYSTEM
from .FNV import fnv32

class Bone(Serializer):
    def read(self, buf: BufferedReader):
        self.matrix = []
        for i in range(16):
            self.matrix.append(uint32_t(buf))

    def write(self, buf: BufferedWriter):
        for i in range(16):
            uint32_t(buf, self.matrix[i])


class WindowsRig(Serializer):
    def read(self, buf: BufferedReader):
        num_bones = uint32_t(buf)

        self.bones = {}

        keys = []
        for i in range(num_bones):
            keys.append(uint32_t(buf))

        for i in range(num_bones):
            self.bones[keys[i]] = Bone()
            self.bones[keys[i]].read(buf)

    def write(self, buf: BufferedWriter):
        start_write()
        uint32_t(buf, len(self.bones))

        keys = list(self.bones.keys())
        for key in keys:
            uint32_t(buf, key)

        for key in keys:
            self.bones[key].write(buf)

class Face(Serializer):
    def read(self, buf: BufferedReader):
        self.a = uint16_t(buf)
        self.b = uint16_t(buf)
        self.c = uint16_t(buf)

    def write(self, buf: BufferedWriter):
        uint16_t(buf, self.a)
        uint16_t(buf, self.b)
        uint16_t(buf, self.c)

FLOAT2 = 1
FLOAT3 = 2
FLOAT = 4

class VertexKey(Serializer):

    offset: int = 0
    type: int = 0
    index: int = 0
    sub_index: int = 0

    def read(self, buf: BufferedReader):
        self.offset = uint32_t(buf)
        self.type = uint8_t(buf)
        self.index = uint8_t(buf)
        self.sub_index = uint8_t(buf)

    def write(self, buf: BufferedWriter):
        pass

class Vertex:
    normal: Vector3 = Vector3()
    position: Vector3 = Vector3()
    uv1: Vector2 = Vector2()
    uv2: Vector2 = Vector2()

    def set_by_index(self, index, value, sub_index):
        if index == 0:
            self.position = value
            return
        
        if index == 1:
            self.normal = value
            return
        
        if index == 2 and sub_index == 0:
            self.uv1 = value
            return
        
        if index == 2 and sub_index == 1:
            self.uv2 = value
            return

class WindowsModelDrawable(Serializer):

    vertices: list[Vertex]
    faces: list[Face]
    vertex_keys: list[VertexKey]

    def read(self, buf: BufferedReader):
        start_read()
        self.material = ResourceKey()
        self.material.read(buf)

        self.bounds_min = Vector3()
        self.bounds_min.read(buf)

        self.bounds_max = Vector3()
        self.bounds_max.read(buf)

        skip(buf, 8)
        self.name = uint32_t(buf)
        skip(buf, 4)
        skip(buf, 12)

        num_verts = uint32_t(buf)
        num_faces = uint32_t(buf)

        self.vertices = []
        self.faces = []

        self.vertex_keys = []

        vertex_key_count = uint32_t(buf)
        for i in range(vertex_key_count):
            key = VertexKey()
            key.read(buf)

            self.vertex_keys.append(key)

        self.vertices = []

        vertex_array_size = uint32_t(buf)
        vertex_size = int(vertex_array_size / num_verts)
        for i in range(0, vertex_array_size, vertex_size):
            start = buf.tell()
            vertex = Vertex()

            for vertex_key in self.vertex_keys:
                buf.seek(start + vertex_key.offset)

                if vertex_key.type == FLOAT2:
                    value = Vector2()
                    value.read(buf)
                    vertex.set_by_index(vertex_key.index, value, vertex_key.sub_index)

                elif vertex_key.type == FLOAT3:
                    value = Vector3()
                    value.read(buf)
                    value.convert_to_blender()
                    vertex.set_by_index(vertex_key.index, value, vertex_key.sub_index)

                elif vertex_key.type == FLOAT:
                    value = float32_t(buf)
                    vertex.set_by_index(vertex_key.index, value, vertex_key.sub_index)

            
            self.vertices.append(vertex)

        uint32_t(buf) # faces_array_size
        for i in range(num_faces):
            face = Face()
            face.read(buf)

            self.faces.append(face)
        self.rig_index = uint32_t(buf) # rig index

    def to_node(self, parent = None, standalone = False):
        mesh_node = bpy.data.meshes.new("mesh")
        obj_node = bpy.data.objects.new("drawable", mesh_node)

        obj_node.mysims_data.object_type = "drawable"

        material: MySimsMaterialProps = obj_node.mysims_data.material
        SetKeyProperty(material, "set_key", self.material)

        bpy.context.collection.objects.link(obj_node)

        bm = bmesh.new()

        # TODO: Fix normals

        uv1 = bm.loops.layers.uv.new("UVMap")

        verts = []

        try:
            for vertex in self.vertices:
                verts.append(bm.verts.new((vertex.position.x, vertex.position.y, vertex.position.z)))

            for face in self.faces:
                v1 = verts[face.a]
                v2 = verts[face.b]
                v3 = verts[face.c]

                bm_face = bm.faces.new((v1, v2, v3))
                bm_face.smooth = True

                bm_face.loops[0][uv1].uv = (self.vertices[face.a].uv1.x, 1.0 - self.vertices[face.a].uv1.y)
                bm_face.loops[1][uv1].uv = (self.vertices[face.b].uv1.x, 1.0 - self.vertices[face.b].uv1.y)
                bm_face.loops[2][uv1].uv = (self.vertices[face.c].uv1.x, 1.0 - self.vertices[face.c].uv1.y)

        except:
            pass

        bm.verts.ensure_lookup_table()
        bm.faces.ensure_lookup_table()
        bm.to_mesh(mesh_node)
        bm.free()

        bpy.context.view_layer.objects.active = obj_node
        obj_node.select_set(True)
        obj_node.parent = parent

        if self.material:
            mat = MySimsMaterial.get(self.material)
            if mat:
                material.materials.clear()
                if isinstance(mat, MySimsMaterial):
                    props: MySimsSingleMaterialProps = material.materials.add()

                    mat.to_node(props)

                    create_material(obj_node, props)

                elif isinstance(mat, MySimsMaterialSet):
                    mat.to_node(material.materials, mat.key)

                    create_material(obj_node, material.materials[0])


    def from_node(self, node: bpy.types.Object):
        if not node or not node.type == 'MESH':
            raise ValueError("Node must be a mesh object")

        self.name = fnv32(node.name)
        self.material = ResourceKey.from_name(0x01d0e75d, node.material.name)

        self.bounds_min = Vector3()
        self.bounds_max = Vector3()

        self.vertices = []
        self.faces = []

        for vertex in node.data.vertices:
            v = Vertex()
            v.position = Vector3(vertex.co.x, vertex.co.y, vertex.co.z)
            v.normal = Vector3(vertex.normal.x, vertex.normal.y, vertex.normal.z)
            v.uv1 = Vector2(vertex.uv[0].x, vertex.uv[0].y)
            v.uv2 = Vector2(vertex.uv[1].x, vertex.uv[1].y)
            self.vertices.append(v)

        for face in node.data.polygons:
            f = Face()
            f.a = face.vertices[0]
            f.b = face.vertices[1]
            f.c = face.vertices[2]
            self.faces.append(f)

    def write_vertex_keys(self, buf):
        start_write()
        uint32_t(buf, 3)

        # position
        uint32_t(buf, 0)
        uint8_t(buf, FLOAT3)
        uint8_t(buf, 0)
        uint8_t(buf, 0)

        # normal
        uint32_t(buf, 12)
        uint8_t(buf, FLOAT3)
        uint8_t(buf, 1)
        uint8_t(buf, 0)

        # uv1
        uint32_t(buf, 24)
        uint8_t(buf, FLOAT2)
        uint8_t(buf, 2)
        uint8_t(buf, 0)

        # uv2
        uint32_t(buf, 32)
        uint8_t(buf, FLOAT2)
        uint8_t(buf, 2)
        uint8_t(buf, 1)

    def write(self, buf: BufferedWriter):
        start_write()
        self.material.write(buf)

        self.bounds_min.write(buf)
        self.bounds_max.write(buf)

        skip(buf, 8)
        uint32_t(buf, self.name)
        uint32_t(buf, 3)
        skip(buf, 12)
        uint32_t(buf, len(self.vertices))
        uint32_t(buf, len(self.faces))
        
        self.write_vertex_keys(buf)

        create_hole(buf, "vertexArraySize", 4)
        vertex_array_size = offset(buf)

        for vertex in self.vertices:
            vertex.position.write(buf)
            vertex.normal.write(buf)
            vertex.uv1.write(buf)
            vertex.uv2.write(buf)

        fill_hole("vertexArraySize", lambda: offset(buf) - vertex_array_size)

        create_hole(buf, "facesArraySize", 4)
        faces_array_size = offset(buf)

        for face in self.faces:
            face.write(buf)

        fill_hole("facesArraySize", lambda: offset(buf) - faces_array_size)

        uint32_t(buf, self.rig_index)

class WindowsModel(Serializer):

    rigs: list[WindowsRig]
    drawables: list[WindowsModelDrawable]

    def __init__(self, path):
        self.path = path
        self.name = os.path.splitext(os.path.basename(path))[0]

    def read(self, buf: BufferedReader):
        start_read()

        skip(buf)
        self.magic = string(buf, 4)
        self.minor_version = uint8_t(buf)
        self.major_version = uint8_t(buf)

        skip(buf, 2)

        self.bounds_min = Vector3()
        self.bounds_min.read(buf)

        self.bounds_max = Vector3()
        self.bounds_max.read(buf)

        num_extra_params = uint32_t(buf)
        self.extra_params = {}

        if(num_extra_params != 0):
            keys = []
            for i in range(num_extra_params):
                keys.append(uint32_t(buf))

            uint32_t(buf) # extra params size
            for i in range(num_extra_params):
                self.extra_params[keys[i]] = cstring(buf)
        else:
            skip(buf)

        self.rigs = []
        self.drawables = []

        num_rigs = uint32_t(buf)
        for i in range(num_rigs):
            rig = WindowsRig()
            rig.read(buf)

            self.rigs.append(rig)

        num_drawables = uint32_t(buf)
        for i in range(num_drawables):
            drawable = WindowsModelDrawable()
            drawable.read(buf)

            self.drawables.append(drawable)

    def to_node(self, parent_node = None, standalone = False, include_physics = False):
        out_node = None
        if standalone:
            for drawable in self.drawables:
                drawable.to_node(parent_node, standalone)
        else:
            holder = bpy.data.objects.new(self.name, None)
            bpy.context.collection.objects.link(holder)

            holder.parent = parent_node

            holder.mysims_data.object_type = "model"

            drawables = bpy.data.objects.new("drawables", None)
            bpy.context.collection.objects.link(drawables)

            drawables.parent = holder

            out_node = holder

            for drawable in self.drawables:
                drawable.to_node(drawables, standalone)

        if include_physics:
            key = ResourceKey.from_file_name(self.name)
            physics_key = ResourceKey(key.group, 0xd5988020, fnv32('CollisionResource'))

            path = MS_FILE_SYSTEM.get(physics_key)

            if path:
                with open(path, "rb") as physics_file:
                    physics = HavokPhysics(str(physics_key))
                    physics.read(physics_file)

                    if standalone:
                        physics.to_node(parent_node)
                    else:
                        physics_holder = bpy.data.objects.new("physics", None)
                        bpy.context.collection.objects.link(physics_holder)

                        physics_holder.parent = holder
                        physics.to_node(physics_holder)

        # same for rigs

        return out_node

    def from_node(self, node):
        pass

    def write(self, buf: BufferedWriter):
        start_write()
        print("Writing WMDL " + self.name)
        uint8_t(buf, 4)
        string(buf, 4, "WMDL")
        uint8_t(buf, 2)
        uint8_t(buf, 1)
        uint16_t(buf, 0)

        self.bounds_min.write(buf)
        self.bounds_max.write(buf)

        uint32_t(buf, len(self.extra_params))
        keys = list(self.extra_params.keys())
        for key in keys:
            uint32_t(buf, key)

        create_hole(buf, "extra_param_value_size", 4)
        extra_param_value_size = offset(buf)

        for key in keys:
            cstring(buf, self.extra_params[key])

        fill_hole("extra_param_value_size", lambda: offset(buf) - extra_param_value_size)

        if len(self.extra_params) == 0:
            uint8_t(buf, 0)

        uint32_t(buf, len(self.rigs))
        for rig in self.rigs:
            rig.write(buf)
        uint32_t(buf, len(self.drawables))
        for drawable in self.drawables:
            drawable.write(buf)
