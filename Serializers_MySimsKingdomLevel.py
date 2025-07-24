from math import radians

from mathutils import Vector, Euler

from .FNV import fnv32
from .Serializers_HavokPhysics import HavokPhysics
from .Serializers_Serializer import Serializer
from .Serializers_WindowsModel import WindowsModel
from .MySimsFileSystem import *
from .util import *


class MySimsSceneObject(Serializer):
    model: WindowsModel | None = None

    def read(self, buf: BufferedReader):
        self.instance = uint64_t(buf)
        model_key = ResourceKey(self.instance, 0xb359c791, 0)
        path = MS_FILE_SYSTEM.get(model_key)

        if path:
            with open(path, 'rb') as file:
                wmdl = WindowsModel(path)
                wmdl.read(file)
                self.model = wmdl

        self.pos = Vector3()
        self.pos.read(buf)
        self.pos.convert_to_blender()

        self.rot = Vector3()
        self.rot.read(buf)
        self.rot.convert_to_blender()

        self.scale = Vector3()
        self.scale.read(buf)
        self.scale.convert_to_blender()

        uint32_t(buf) # zero?

    def write(self, buf: BufferedWriter):
        pass

    def to_node(self, parent_node = None):
        if self.model:
            obj = self.model.to_node(parent_node)

            obj.location = Vector((self.pos.x,self.pos.y,self.pos.z))
            obj.rotation_euler = Euler(Vector((radians(self.rot.x), radians(self.rot.y), radians(self.rot.z))), "XYZ")
            obj.scale = Vector((self.scale.x,self.scale.y,self.scale.z))

            return obj
        return None


class MySimsKingdomLevel(Serializer):
    name: str
    path: str
    models: list[WindowsModel] = []
    objects: list[MySimsSceneObject] = []

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def read(self, buf: BufferedReader):
        string(buf, 4) # LLMF
        uint32_t(buf)

        startPosX = float32_t(buf)
        startPosZ = float32_t(buf)

        cellSizeX = uint32_t(buf)
        cellSizeZ = uint32_t(buf)

        numCellsX = uint32_t(buf)
        numCellsZ = uint32_t(buf)

        float32_t(buf)
        float32_t(buf)

        model_count = uint32_t(buf)
        object_count = uint32_t(buf)

        bounds_min = Vector3()
        bounds_min.read(buf)

        bounds_max = Vector3()
        bounds_max.read(buf)

        self.objects = []
        self.models = []

        for i in range(model_count):
            instance = uint64_t(buf)
            model_key = ResourceKey(instance, 0xb359c791, 0)
            path = MS_FILE_SYSTEM.get(model_key)

            if path:
                with open(path, 'rb') as file:
                    wmdl = WindowsModel(path)
                    wmdl.read(file)
                    self.models.append(wmdl)

        for i in range(object_count):
            object = MySimsSceneObject()
            object.read(buf)
            self.objects.append(object)


    def write(self, buf: BufferedWriter):
        pass

    def to_node(self, parent_node = None, include_physics = False):
        level_node = bpy.data.objects.new(self.name, None)
        bpy.context.collection.objects.link(level_node)

        level_node.parent = parent_node
        level_node.mysims_data.object_type = "level"

        model_node = bpy.data.objects.new("models", None)
        bpy.context.collection.objects.link(model_node)
        model_node.parent = level_node

        for models in self.models:
            models.to_node(model_node)

        objects_node = bpy.data.objects.new("objects", None)
        bpy.context.collection.objects.link(objects_node)
        objects_node.parent = level_node

        for object in self.objects:
            object.to_node(objects_node)

        if include_physics:
            physics_key = ResourceKey.from_file_name(self.path)
            physics_key.type = 0xd5988020

            path = MS_FILE_SYSTEM.get(physics_key)

            if path:
                with open(path, "rb") as physics_file:
                    physics = HavokPhysics(str(physics_key))
                    physics.read(physics_file)

                    physics_holder = bpy.data.objects.new("physics", None)
                    bpy.context.collection.objects.link(physics_holder)

                    physics_holder.parent = level_node
                    physics.to_node(physics_holder)

        return level_node