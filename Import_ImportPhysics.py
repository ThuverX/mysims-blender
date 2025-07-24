import os
from bpy.props import StringProperty, CollectionProperty
from bpy.types import Operator, PropertyGroup
from bpy_extras.io_utils import ImportHelper

from .Serializers_HavokPhysics import HavokPhysics


import sys
sys.path.append("//")
import havokpy

class ImportPhysics(Operator, ImportHelper):

    bl_idname = "import_mesh.physics"
    bl_label = "Import MySims WindowsModel"
    bl_description = "Load a Windows Model"
    bl_options = {'UNDO'}
    filename_ext = (".Physics")

    files: CollectionProperty(type=PropertyGroup) 
    filter_glob: StringProperty(default="*.Physics", options={'HIDDEN'})

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
        with open(path, 'rb') as file:
            physics = HavokPhysics(path)
            physics.read(file)
            physics.to_node()
