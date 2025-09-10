bl_info = {
    "name": "Quick Fullscreen",
    "author": "SHARIAR",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Quick Tools",
    "description": "Adds a button in the sidebar to toggle fullscreen for 3D View",
    "category": "Interface",
}

import bpy


class View3D_Quick_Fullscreen(bpy.types.Operator):
    """Toggle Fullscreen Area"""
    bl_idname = "view3d.quick_fullscreen_sidebar"
    bl_label = "Toggle Fullscreen"

    def execute(self, context):
        # Find the first 3D View area
        for area in context.window.screen.areas:
            if area.type == 'VIEW_3D':
                with context.temp_override(area=area):
                    bpy.ops.screen.screen_full_area(use_hide_panels=False)
                break
        return {'FINISHED'}


class View3D_Quick_Fullscreen_Panel(bpy.types.Panel):
    """Sidebar Panel for Quick Fullscreen"""
    bl_label = "Quick Full Screen"
    bl_idname = "VIEW3D_PT_quick_fullscreen"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Full Screen"

    def draw(self, context):
        layout = self.layout
        layout.operator("view3d.quick_fullscreen_sidebar", icon="FULLSCREEN_ENTER")


def register():
    bpy.utils.register_class(View3D_Quick_Fullscreen)
    bpy.utils.register_class(View3D_Quick_Fullscreen_Panel)


def unregister():
    bpy.utils.unregister_class(View3D_Quick_Fullscreen_Panel)
    bpy.utils.unregister_class(View3D_Quick_Fullscreen)


if __name__ == "__main__":
    register()
