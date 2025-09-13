from bpy.types import Panel

from .Props_ObjectProps import MySimsObjectProps

class MySimsPanelObject(Panel):
    bl_label = "Object Settings"
    bl_idname = "OBJECT_PT_mysims_object"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MySims"

    def draw(self, context):
        layout = self.layout
        object = context.object

        if object is None:
            return
        
        if object.type != 'MESH' and object.type != 'EMPTY':
            return
        
        object_props: MySimsObjectProps = object.mysims_data

        if object_props is None:
            return

        layout.prop(object_props, "object_type", text="Object Type")

        if object_props.object_type == 'physics':
            layout.prop(object_props, "physics_type", text="Physics Type")

        if object_props.object_type == 'level':
            layout.operator("mysims.copy_material", text="Bake ambient map (shadows)")

        if object_props.object_type == 'model':
            layout.operator("export_mesh.windowsmodel", text="Export")
