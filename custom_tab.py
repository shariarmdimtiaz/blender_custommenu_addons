bl_info = {
    "name": "Custom Side Tab",
    "blender": (3, 0, 0),
    "category": "3D View",
    "author": "SHARIAR",
    "description": "Adds a custom tab in the sidebar with a button",
}

import bpy
import subprocess
import os

# Path to your batch file (update this!)
BAT_FILE = r"C:\demo\apps.bat"

# To run batch file
class CUSTOM_Apps_Run(bpy.types.Operator):
    bl_idname = "custom.run_apps"
    bl_label = "Run Apps"

    def execute(self, context):
        if os.path.exists(BAT_FILE):
            subprocess.Popen([BAT_FILE], shell=True)
            self.report({'INFO'}, "COLMAP started")
        else:
            self.report({'ERROR'}, f"File not found: {BAT_FILE}")
        return {'FINISHED'}


# Panel in the sidebar
class CUSTOM_PT_Sidebar(bpy.types.Panel):
    bl_label = "Custom Tools"           # Panel title
    bl_idname = "CUSTOM_PT_Sidebar"     
    bl_space_type = 'VIEW_3D'           # 3D Viewport
    bl_region_type = 'UI'               # Sidebar region
    bl_category = "Custom Tools"        # Tab name (appears as new tab in "N" panel)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Run External Tools")
        layout.operator("custom.run_apps", text="Generate Outside Mesh")


# Register
def register():
    bpy.utils.register_class(CUSTOM_Apps_Run)
    bpy.utils.register_class(CUSTOM_PT_Sidebar)


# Unregister
def unregister():
    bpy.utils.unregister_class(CUSTOM_PT_Sidebar)
    bpy.utils.unregister_class(CUSTOM_Apps_Run)


if __name__ == "__main__":
    register()
