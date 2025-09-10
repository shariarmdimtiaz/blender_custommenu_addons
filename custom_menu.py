bl_info = {
    "name": "Custom Menu",
    "blender": (3, 0, 0),
    "category": "3D View",
    "author": "SHARIAR",
    "description": "Adds a custom menu to the Add menu in blender and removes it on unregister",
}

import bpy
import subprocess
import os

# Path to the application's colmap.bat file (update this!)
BAT_FILE = r"C:\demo\apps.bat"

# Define a custom operator to run the batch file
class CUSTOM_Apps_Run(bpy.types.Operator):
    bl_idname = "custom.run_apps"
    bl_label = "Generate Mesh"

    def execute(self, context):
        if os.path.exists(BAT_FILE):
            try:
                subprocess.Popen([BAT_FILE], shell=True)
                self.report({'INFO'}, f"Running {BAT_FILE}")
            except Exception as e:
                self.report({'ERROR'}, f"Failed: {e}")
        else:
            self.report({'ERROR'}, f"File not found: {BAT_FILE}")
        return {'FINISHED'}


# Define a custom menu
class CUSTOM_MT_add_menu(bpy.types.Menu):
    bl_label = "CUSTOM Menu"
    bl_idname = "CUSTOM_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.primitive_cube_add", text="Add Cube")
        layout.operator("mesh.primitive_uv_sphere_add", text="Add Sphere")
        layout.operator("mesh.primitive_cone_add", text="Add Cone")
        layout.operator("custom.run_apps", text="Generate Mesh")  # <-- custom operator here


# Function to hook menu into "Add" menu
def add_menu(self, context):
    self.layout.menu(CUSTOM_MT_add_menu.bl_idname)


# Register
def register():
    bpy.utils.register_class(CUSTOM_Apps_Run)
    bpy.utils.register_class(CUSTOM_MT_add_menu)
    bpy.types.VIEW3D_MT_add.append(add_menu)

# Unregister
def unregister():
    bpy.types.VIEW3D_MT_add.remove(add_menu)
    bpy.utils.unregister_class(CUSTOM_MT_add_menu)
    bpy.utils.unregister_class(CUSTOM_Apps_Run)


if __name__ == "__main__":
    register()