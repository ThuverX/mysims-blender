import os
import bpy

from io import BufferedReader, BufferedWriter

from ..havokpy2.classes.shapes.hkSimpleMeshShape import hkSimpleMeshShapeClass
from ..havokpy2.classes.shapes.hkSphereShape import hkSphereShapeClass
from ..havokpy2.classes.shapes.hkMoppBvTreeShape import hkMoppBvTreeShapeClass
from ..havokpy2.HavokFile import HavokFileReader

class HavokPhysics:
    def __init__(self, path):
        self.path = path

    def read_shape(self, shape):
        if shape is None:
            return
        
        if isinstance(shape, hkMoppBvTreeShapeClass):
            self.read_shape(shape.childShape)

        elif isinstance(shape, hkSimpleMeshShapeClass):
            self.shapes.append(shape)

        elif isinstance(shape, hkSphereShapeClass):
            self.shapes.append(shape)

    def shape_to_node(self, shape, parent_node = None):
        if shape is None:
            return

        if isinstance(shape, hkMoppBvTreeShapeClass):
            self.read_shape(shape.childShape)

        elif isinstance(shape, hkSimpleMeshShapeClass):
            verts = [(-v.x, v.z, v.y) for v in shape.vertices]
            faces = [(f.a, f.b, f.c) for f in shape.triangles]

            mesh = bpy.data.meshes.new("ShapeMesh")
            mesh.from_pydata(verts, [], faces)
            mesh.update()

            obj = bpy.data.objects.new("hkSimpleMeshShape", mesh)
            obj.parent = parent_node

            bpy.context.collection.objects.link(obj)

            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            obj.mysims_data.object_type = 'physics'
            obj.mysims_data.physics_type = 'hkSimpleMeshShape'


        elif isinstance(shape, hkSphereShapeClass):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=shape.radius, enter_editmode=False, location=(0, 0, 0))
            sphere_obj = bpy.context.active_object
            sphere_obj.name = "hkSphereShape"

            sphere_obj.mysims_data.object_type = 'physics'
            sphere_obj.mysims_data.physics_type = 'hkSphereShape'

            sphere_obj.parent = parent_node


    def read(self, buf: BufferedReader):
        reader = HavokFileReader()
        havok_file = reader.read(buf)
        self.shapes = []
        # entries 0???
        data_section = havok_file.fileEntries[0].sections[1]
        for system in data_section.root.systems:
            for rigid_body in system.rigidbodies:
                self.read_shape(rigid_body.shape)

    def to_node(self, parent_node = None):
        for shape in self.shapes:
            self.shape_to_node(shape, parent_node)

    def write(self, buf: BufferedWriter):
        pass