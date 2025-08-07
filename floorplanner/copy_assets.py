import bpy
import os
import shutil
from bpy.types import AddonPreferences, Operator
from bpy.props import StringProperty


def get_user_library_path():
    for lib in bpy.context.preferences.filepaths.asset_libraries:
        if lib.name == "User Library":
            return bpy.path.abspath(lib.path)
    return None


class JOHNNYGIZMO_FloorPlanner_OT_copy_assets(Operator):
    bl_idname = "myaddon.copy_assets_to_user_library"
    bl_label = "Copy Assets to 'User Library'"
    bl_description = "Copies the bundled assets.blend to the User Library Asset Folder"

    @classmethod
    def poll(self, context):
        return get_user_library_path() is not None

    def execute(self, context):
        user_lib_path = get_user_library_path()

        if not user_lib_path:
            self.report({'ERROR'}, "User Library not found in Asset Libraries.")
            return {'CANCELLED'}

        addon_dir = os.path.dirname(__file__)
        source_file = os.path.join(addon_dir, "FloorPlanner3.blend")
        target_file = os.path.join(user_lib_path, "FloorPlanner3.blend")

        if not os.path.exists(source_file):
            self.report({'ERROR'}, "FloorPlanner3.blend not found in the add-on directory.")
            return {'CANCELLED'}

        try:
            shutil.copyfile(source_file, target_file)
            self.report({'INFO'}, f"Copied FloorPlanner3.blend to {target_file}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to copy: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}




def register():
    bpy.utils.register_class(JOHNNYGIZMO_FloorPlanner_OT_copy_assets)

def unregister():
    bpy.utils.unregister_class(JOHNNYGIZMO_FloorPlanner_OT_copy_assets)
