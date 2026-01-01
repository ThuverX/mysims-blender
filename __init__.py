import bpy
from bpy.types import Object, Scene
from bpy.props import PointerProperty

from .Export.ExportWindowsModel import ExportWindowsModel
from .Operators.EnableMySimsMaterial import EnableMySimsMaterial
from .UI.MaterialParamList import MATERIAL_UL_param_list
from .UI.MaterialList import MATERIAL_UL_list
from .Operators.CopyMySimsMaterial import CopyMySimsMaterial
from .Shaders.ShaderNodes import register_shaders, unregister_shaders
from .Props.MaterialProps import MySimsMaterialProps, MySimsMaterialParam, MySimsSingleMaterialProps
from .Props.ObjectProps import MySimsObjectProps
from .Props.SceneProps import MySimsSceneProps

from .MySimsFileSystem import MS_FILE_SYSTEM
from .Props.KeyProp import BlenderKeyProperty
from .Panels.MySimsPanelMain import MySimsPanelMain
from .Panels.MySimsPanelObject import MySimsPanelObject
from .Panels.MySimsPanelMaterial import MySimsPanelMaterial

from .Import.ImportWindowsModel import ImportWindowsModel
from .Import.ImportPhysics import ImportPhysics
from .Import.ImportMySimsLevel import ImportMySimsLevel

bl_info = {
    "name": "MySims Blender",
    "blender": (4, 3, 2),
    "category": "Import/Export"
}

def menu_import(self, _):
    self.layout.operator(ImportWindowsModel.bl_idname, text="MySims WindowsModel (.windowsmodel)")
    self.layout.operator(ImportPhysics.bl_idname, text="MySims Physics (.Physics)")
    self.layout.operator(ImportMySimsLevel.bl_idname, text="MySims Level (.levelxml)")

# # def menu_export(self, _):
# #     self.layout.operator(ExportWindowsModel.bl_idname, text="MySims WindowsModel (.windowsmodel)")


classes = [
    BlenderKeyProperty,

    MATERIAL_UL_param_list,
    MATERIAL_UL_list,

    MySimsMaterialParam,
    MySimsSingleMaterialProps,
    MySimsMaterialProps,
    MySimsObjectProps,
    MySimsSceneProps,

    CopyMySimsMaterial,
    EnableMySimsMaterial,

    ImportPhysics,
    ImportWindowsModel,
    ImportMySimsLevel,
    ExportWindowsModel,

    MySimsPanelMain,
    MySimsPanelObject,
    MySimsPanelMaterial
]

def update_timer():
    scene = bpy.context.scene
    scene_props: MySimsSceneProps = scene.mysims_data

    if len(scene_props.game_path) <= 0:
        return None

    MS_FILE_SYSTEM.update()
    
    return None


def create_shaders(a = None,b = None):
    register_shaders()
    return None

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    Object.mysims_data = PointerProperty(type=MySimsObjectProps)
    Scene.mysims_data = PointerProperty(type=MySimsSceneProps)

    bpy.types.TOPBAR_MT_file_import.append(menu_import)
    # bpy.types.TOPBAR_MT_file_export.append(menu_export)

    bpy.app.timers.register(create_shaders)
    bpy.app.handlers.load_post.append(create_shaders)
    bpy.app.handlers.load_factory_startup_post.append(create_shaders)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.TOPBAR_MT_file_import.remove(menu_import)
    # bpy.types.TOPBAR_MT_file_export.remove(menu_export)
    del Object.mysims_data
    del Scene.mysims_data

    unregister_shaders()



if __name__ == "__main__":
    register()