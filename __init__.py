import bpy
from bpy.types import Material, Object, Scene
from bpy.props import PointerProperty

from .Export_ExportWindowsModel import ExportWindowsModel
from .Operators_EnableMySimsMaterial import EnableMySimsMaterial
from .UI_MaterialParamList import MATERIAL_UL_param_list
from .UI_MaterialList import MATERIAL_UL_list
from .Operators_CopyMySimsMaterial import CopyMySimsMaterial
from .Shaders_ShaderNodes import register_shaders, unregister_shaders
from .Props_MaterialProps import MySimsMaterialProps, MySimsMaterialParam, MySimsSingleMaterialProps
from .Props_ObjectProps import MySimsObjectProps
from .Props_SceneProps import MySimsSceneProps

from .MySimsFileSystem import MS_FILE_SYSTEM
from .Props_KeyProp import BlenderKeyProperty
from .Panels_MySimsPanelMain import MySimsPanelMain
from .Panels_MySimsPanelObject import MySimsPanelObject
from .Panels_MySimsPanelMaterial import MySimsPanelMaterial

from .Import_ImportWindowsModel import ImportWindowsModel
from .Import_ImportPhysics import ImportPhysics
from .Import_ImportMySimsLevel import ImportMySimsLevel

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