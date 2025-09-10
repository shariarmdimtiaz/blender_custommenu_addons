bl_info = {
    "name": "Custom Menu",
    "blender": (3, 0, 0),
    "category": "3D View",
    "author": "SHARIAR",
    "description": "Adds a custom menu to the Add menu and removes it on unregister",
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


