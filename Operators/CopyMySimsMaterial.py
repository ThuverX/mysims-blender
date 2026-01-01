from bpy.types import Operator
from bpy.props import IntProperty

from ..Props.MaterialProps import MySimsMaterialProps

import bpy

def deep_copy_property_group(src, dst_collection):
    """Deep copies a PropertyGroup item (with nested pointers and collections) into dst_collection."""
    new_item = dst_collection.add()

    for prop in src.bl_rna.properties:
        if prop.identifier == "rna_type":
            continue  # Skip Blender's internal property

        value = getattr(src, prop.identifier)
        prop_type = type(prop)

        if isinstance(prop, bpy.types.CollectionProperty):
            dst_sub_collection = getattr(new_item, prop.identifier)
            for sub_item in value:
                deep_copy_property_group(sub_item, dst_sub_collection)

        elif isinstance(prop, bpy.types.PointerProperty):
            dst_pointer = getattr(new_item, prop.identifier)
            deep_copy_into_pointer(value, dst_pointer)

        else:
            try:
                setattr(new_item, prop.identifier, value)
            except Exception:
                pass  # Ignore properties that aren't writable

    return new_item

def deep_copy_into_pointer(src_pointer, dst_pointer):
    """Copies data into a PointerProperty target."""
    if not src_pointer or not dst_pointer:
        return

    for prop in src_pointer.bl_rna.properties:
        if prop.identifier == "rna_type":
            continue

        value = getattr(src_pointer, prop.identifier)
        if isinstance(prop, bpy.types.CollectionProperty):
            dst_sub_collection = getattr(dst_pointer, prop.identifier)
            for sub_item in value:
                deep_copy_property_group(sub_item, dst_sub_collection)

        elif isinstance(prop, bpy.types.PointerProperty):
            deep_copy_into_pointer(value, getattr(dst_pointer, prop.identifier))

        else:
            try:
                setattr(dst_pointer, prop.identifier, value)
            except Exception:
                pass

class CopyMySimsMaterial(Operator):
    bl_idname = "mysims.copy_material"
    bl_label = "Copy a mysims material"

    index: IntProperty(default=-1)

    def execute(self, context):
        obj = context.object
        material_props: MySimsMaterialProps = obj.mysims_data.material

        index = self.index

        if index == -1:
            index = material_props.selected_material
        else:
            material_props.selected_material = index

        new_item = deep_copy_property_group(material_props.materials[index], material_props.materials)

        material_props.selected_material = len(material_props.materials) - 1

        new_item.locked = False
        new_item.key.key = ""


        return {'FINISHED'}
