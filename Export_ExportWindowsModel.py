from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportWindowsModel(Operator, ExportHelper):
    bl_idname = "export_mesh.windowsmodel"
    bl_label = "Export MySims WindowsModel"

    filename_ext = ".windowsmodel"
    filter_glob: StringProperty(default="*.windowsmodel;*.wmdl;*.0xb359c791", options={'HIDDEN'})
    selected: BoolProperty(default=True, description="", name="Include Selection Only")

    def execute(self, context):
        # if only one object
        #  that one object is drawable 1
        # if only one root empty
        #  that empty is the main object
        # if the main object has multiple children
        #  then each of those children are a drawable

        
    
        pass
