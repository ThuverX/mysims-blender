from bpy.types import PropertyGroup
from bpy.props import StringProperty


class MySimsSceneProps(PropertyGroup):
    game_path: StringProperty(subtype='DIR_PATH', name="Game Folder",
                              default="C:/Program Files (x86)/Steam/steamapps/common/MySims/data/")
