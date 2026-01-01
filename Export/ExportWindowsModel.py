from os import write

from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

from ..Serializers.WindowsModel import WindowsModel


class ExportWindowsModel(Operator, ExportHelper):
    bl_idname = "export_mesh.windowsmodel"
    bl_label = "Export MySims WindowsModel"

    filename_ext = ".0xb359c791"
    filter_glob: StringProperty(default="*.windowsmodel;*.wmdl;*.0xb359c791", options={'HIDDEN'})
    selected: BoolProperty(default=True, description="", name="Include Selection Only")

    def execute(self, context):
        obj = context.object

        windowsmodel = WindowsModel(self.filepath)
        windowsmodel.from_node(obj)

        with open(windowsmodel.path, 'wb') as file:
            windowsmodel.write(file)

        return {'FINISHED'}
