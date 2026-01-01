from bpy.types import PropertyGroup
from bpy.props import StringProperty, EnumProperty,IntProperty, FloatProperty


class HavokPhysicsProps(PropertyGroup):
    response_type: IntProperty(name="Response type")
    friction: FloatProperty(name="Friction")
    restitution: FloatProperty(name="Restitution")