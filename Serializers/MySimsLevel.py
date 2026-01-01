import xml.etree.ElementTree as ET
from io import BufferedWriter
import bpy

from .HavokPhysics import HavokPhysics
from ..FNV import fnv32
from .Serializer import Serializer
from .WindowsModel import WindowsModel
from ..MySimsFileSystem import *

class MySimsLevel(Serializer):

    name: str
    models: list[WindowsModel] = []

    def __init__(self, path):
        self.path = path

    def read(self, buf: BufferedReader):
        print("Loading mysims model")

        tree = ET.parse(buf)
        root = tree.getroot()
        self.models = []

        grid_info = root.find("GridInfo")

        model_name = grid_info.find("ModelName").text
        self.name = model_name

        grid_cells = root.find("GridCells")
        models = grid_cells.findall("Model")
        for model in models:
            instance = int(model.text)
            model_key = ResourceKey(1, 0xb359c791, instance)
            path = MS_FILE_SYSTEM.get(model_key)

            if path:
                with open(path, 'rb') as file:
                    wmdl = WindowsModel(path)
                    wmdl.read(file)
                    self.models.append(wmdl)

    def write(self, buf: BufferedWriter):
        pass

    def to_node(self, include_physics = False):
        level_node = bpy.data.objects.new(self.name, None)
        bpy.context.collection.objects.link(level_node)

        level_node.mysims_data.object_type = "level"

        model_node = bpy.data.objects.new("models", None)
        bpy.context.collection.objects.link(model_node)
        model_node.parent = level_node

        for models in self.models:
            models.to_node(model_node)

        if include_physics:
            physics_key = ResourceKey(fnv32(self.name), 0xd5988020, 0xc6156fcb)

            path = MS_FILE_SYSTEM.get(physics_key)

            if path:
                with open(path, "rb") as physics_file:
                    physics = HavokPhysics(str(physics_key))
                    physics.read(physics_file)

                    physics_holder = bpy.data.objects.new("physics", None)
                    bpy.context.collection.objects.link(physics_holder)

                    physics_holder.parent = level_node
                    physics.to_node(physics_holder)