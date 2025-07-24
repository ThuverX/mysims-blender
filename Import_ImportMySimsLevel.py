import bpy
import logging

from bpy.props import StringProperty, CollectionProperty
from bpy.types import Operator, PropertyGroup
from bpy_extras.io_utils import ImportHelper

from .Serializers_MySimsKingdomLevel import MySimsKingdomLevel
from .Serializers_MySimsLevel import MySimsLevel
from .MySimsFileSystem import *


def read_xml_model(path):
    with open(path, 'rb') as file:
        level = MySimsLevel(path)
        level.read(file)
        level.to_node(include_physics=True)


def read_bin_model(path):
    filename = os.path.basename(path)
    name = os.path.splitext(filename)[0]
    with open(path, 'rb') as file:
        level = MySimsKingdomLevel(name, path)
        level.read(file)
        level.to_node(include_physics=True)


class ImportMySimsLevel(Operator, ImportHelper):

    bl_idname = "import_mesh.level"
    bl_label = "Import MySims Level"
    bl_description = "Load a MySims Level"
    bl_options = {'UNDO'}
    filename_ext = (".levelxml", ".levelbin")

    files: CollectionProperty(type=PropertyGroup) 
    filter_glob: StringProperty(default="*.xml;*.levelxml;*.levelbin", options={'HIDDEN'})

    def execute(self, context):
        if self.files:
            folder = os.path.dirname(self.filepath)
            for f in self.files:
                path = os.path.join(folder, f.name)
                self.load(path)
        else:
            self.load(self.filepath)

        return {'FINISHED'}
    
    def load(self, path):
        extension = os.path.splitext(path)[1]

        if extension.lower() == ".levelxml":
            read_xml_model(path)
        if extension.lower() == ".levelbin":
            read_bin_model(path)
    
