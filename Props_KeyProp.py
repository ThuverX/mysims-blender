from bpy.props import StringProperty, PointerProperty
from bpy.types import PropertyGroup, UILayout
from .MySimsFileSystem import *
from .Serializers_ResourceKey import ResourceKey, typeid_to_typename


def key_property_updater(self, context):
    key = ResourceKey.from_file_name(self.key)
    exists = MS_FILE_SYSTEM.exists(key)
    if not MS_FILE_SYSTEM.ready:
        self.state = "FAILED"
        return

    if exists:
        self.state = "EXISTS"
    elif typeid_to_typename(key.type) == "Unknown":
        self.state = "UNKNOWN"
    else:
        self.state = "GOOD"


class BlenderKeyProperty(PropertyGroup):
    key: StringProperty(name="Key", update=key_property_updater, default="")
    state: StringProperty("UNKNOWN")


def KeyProperty(name="Key", update=None):
    return PointerProperty(type=BlenderKeyProperty, update=update, name=name)


def SetKeyProperty(props, name, value):
    prop = getattr(props, name, None)
    if isinstance(value, str):
        prop.key = value
    if isinstance(value, ResourceKey):
        prop.key = str(value)


def DrawKeyProperty(props, name, layout: UILayout, display_name="Key", only_errors=False, show_creation=False,
                    custom_error=None):
    area = layout.column()
    prop = getattr(props, name, None)

    area.prop(prop, "key", text=display_name)
    if (
            (prop.state != "GOOD" and (not only_errors or prop.state != "EXISTS"))
            or (show_creation and prop.state == "GOOD")
            or (custom_error is not None and custom_error is not "")
    ):
        box = area.box()
        box.enabled = False
        if custom_error is not None and custom_error is not "":
            box.label(text=custom_error, icon="ERROR")
        elif prop.state == "EXISTS":
            box.label(text="This key uses an existing value", icon="INFO")
        elif prop.state == "FAILED":
            box.alert = True
            box.label(text="Database isn't loaded, did you set a valid game path?", icon="ERROR")
            box.alert = False
        elif prop.state == "GOOD":
            box.label(text="This material will be created on export", icon="INFO")
        else:
            box.label(text="This key is missing a valid type", icon="ERROR")
        box.enabled = True
