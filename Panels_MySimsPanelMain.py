from bpy.types import Panel
from .Props_SceneProps import MySimsSceneProps

class MySimsPanelMain(Panel):
    bl_label = "MySims Settings"
    bl_idname = "OBJECT_PT_mysims_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "MySims"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        if scene is None:
            return
        
        scene_props: MySimsSceneProps = scene.mysims_data

        layout.prop(scene_props, "game_path")

        layout.label(text="Export Settings")
        box = layout.box()


