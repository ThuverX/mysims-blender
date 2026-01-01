from bpy.types import PropertyGroup
from bpy.props import StringProperty, EnumProperty
from ..MySimsFileSystem import MS_FILE_SYSTEM

def on_path_update(self, context):
    MS_FILE_SYSTEM.update()

class MySimsSceneProps(PropertyGroup):
    game_path: StringProperty(subtype='DIR_PATH', name="Game Folder",
                              default="C:/Program Files (x86)/Steam/steamapps/common/MySims/data/",
                              update=on_path_update)
    export_type: EnumProperty(name="Export Type", items=[
        ("default", "Default", ""),
        ("mod", "MSML", "Support for MSML file types")
    ])
