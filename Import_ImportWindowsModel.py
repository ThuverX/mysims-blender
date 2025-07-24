import bpy
import logging
from bpy.props import StringProperty, CollectionProperty
from bpy.types import Operator, PropertyGroup
from bpy_extras.io_utils import ImportHelper

from .MySimsFileSystem import *

from .Serializers_WindowsModel import WindowsModel
from .Serializers_ResourceKey import ResourceKey
from .Serializers_HavokPhysics import HavokPhysics
from .FNV import fnv32

class ImportWindowsModel(Operator, ImportHelper):

    bl_idname = "import_mesh.windowsmodel"
    bl_label = "Import MySims WindowsModel"
    bl_description = "Load a Windows Model"
    bl_options = {'UNDO'}
    filename_ext = (".windowsmodel", ".wmdl", ".0xb359c791")

    files: CollectionProperty(type=PropertyGroup) 
    filter_glob: StringProperty(default="*.windowsmodel;*.wmdl;*.0xb359c791", options={'HIDDEN'})

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
            wmdl = WindowsModel(path)
            wmdl.read(file)
            wmdl.to_node(include_physics=True)
