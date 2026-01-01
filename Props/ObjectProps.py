from bpy.types import PropertyGroup
from bpy.props import EnumProperty, PointerProperty
from .MaterialProps import MySimsMaterialProps

class MySimsObjectProps(PropertyGroup):
    object_type: EnumProperty(name="Object Type",
                              items=[
                                  ('none', "None", ""),
                                  ('level', "Level", ""),
                                  ('model', "Model", ""),
                                  ('drawable', "Drawable", ""),
                                  ('physics', "Physics", ""),
                              ])
    physics_type: EnumProperty(name="Physics Type",
                               items=[
                                   ('hkSphereShape', "hkSphereShape", ""),
                                   ('hkSimpleMeshShape','hkSimpleMeshShape', "")
                               ])
    material: PointerProperty(type=MySimsMaterialProps)
