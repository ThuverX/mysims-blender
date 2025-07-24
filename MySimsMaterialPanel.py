# import bpy
# import bmesh
#
# from bpy.types import Panel, PropertyGroup, Operator, UIList, UILayout
# from bpy.props import StringProperty, EnumProperty, IntProperty, FloatVectorProperty, CollectionProperty, BoolProperty
# from .MySimsShaders import get_shader_list_as_enum
# from ..Props.KeyProp import KeyProperty, DrawKeyProperty
#
# class MySimsMaterialParam(PropertyGroup):
#     name: StringProperty(name="Name")
#     type: EnumProperty(name="Type", items=[
#         ("color","Color",""),
#         ("integer","Integer",""),
#         ("map","Map","")
#     ])
#     color: FloatVectorProperty(name="Color", subtype="COLOR", size=4)
#     map: StringProperty(name="Map", subtype="FILE_PATH")
#     integer: IntProperty(name="Integer")
#
# class MySimsMaterialProps(PropertyGroup):
#     shader_type: EnumProperty(name="Shader", items=get_shader_list_as_enum())
#     key: KeyProperty()
#     params: CollectionProperty(name="Params", type=MySimsMaterialParam)
#     selected_param: IntProperty(name="Index", default=0)
#     has_mysims_material:BoolProperty(name="Has MySims Material")
#
#
# def update_material():
#     obj = bpy.context.active_object
#     mat = obj.active_material
#
#     if obj and obj.type == 'MESH' and mat:
#         try:
#             mat_index = obj.data.materials[:].index(mat)
#         except ValueError:
#             print("Material not found on object")
#         else:
#             bpy.ops.object.mode_set(mode='EDIT')
#
#             mesh = bmesh.from_edit_mesh(obj.data)
#
#             for face in mesh.faces:
#                 face.select = True
#                 face.material_index = mat_index
#
#             bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
#
#             bpy.ops.object.mode_set(mode='OBJECT')
#
#     return None
#
# class MySimsMaterialCreationOperator(Operator):
#     bl_idname = "my_sims.create_material"
#     bl_label = "Create a MySims material"
#     bl_description = "Create a MySims material for this material"
#     bl_options = {"REGISTER"}
#
#     @classmethod
#     def poll(cls, context):
#         return True
#
#     def execute(self, context):
#         mat = context.material
#
#         if mat:
#             props: MySimsMaterialProps = mat.mysims_data
#             props.has_mysims_material = True
#             props.shader_type = "0x94773578"
#
#             # TODO: Append default params, and lambert shader
#             # if it has a texture, put that into diffuse slot
#
#         return {"FINISHED"}
#
# class MySimsMaterialPreviewOperator(Operator):
#     bl_idname = "my_sims.preview_material"
#     bl_label = "Preview a MySims material"
#     bl_description = "Preview a MySims material for this material"
#     bl_options = {"REGISTER"}
#
#     @classmethod
#     def poll(cls, context):
#         return True
#
#     def execute(self, context):
#         mat = context.material
#
#         if mat:
#             update_material()
#
#         return {"FINISHED"}
#
#
# # TODO: Implement this
# class MySimsParam_UL_items(UIList):
#     def draw_item(self, context, layout: UILayout, data, item, icon, active_data, active_propname, index):
#         layout.label(text=f"Some Name ({item.name})")
#
#
# class MySimsMaterialPanel(Panel):
#     bl_label = "MySims Material"
#     bl_idname = "MATERIAL_PT_mysims"
#     bl_space_type = 'PROPERTIES'
#     bl_region_type = 'WINDOW'
#     bl_context = "material"
#     bl_category = "mysims_material"
#     bl_options = {'DEFAULT_CLOSED'}
#
#     def draw(self, context):
#         layout = self.layout
#         mat = context.material
#
#         if mat and mat.mysims_data and mat.mysims_data.has_mysims_material:
#             props: MySimsMaterialProps = mat.mysims_data
#
#             layout.operator("my_sims.preview_material", text="Preview Material")
#
#             layout.prop(props, "shader_type")
#             DrawKeyProperty(props, self, context)
#
#             layout.label(text= "Parameters:")
#             layout.template_list(
#                 "MySimsParam_UL_items",
#                 "material_params",
#                 props, "params",
#                 props, "selected_param",
#             )
#
#             if props.params and props.selected_param >= 0 and props.selected_param < len(props.params):
#                 box = layout.box()
#                 param = props.params[props.selected_param]
#
#                 box.prop(param, "name")
#                 box.prop(param, "type")
#
#                 if param.type == "color":
#                     box.prop(param, "color")
#
#                 if param.type == "integer":
#                     box.prop(param, "integer")
#
#                 if param.type == "map":
#                     box.prop(param, "map")
#
#         else:
#             layout.label(text="This material has no MySims Material")
#             layout.operator("my_sims.create_material", text="Create one?")