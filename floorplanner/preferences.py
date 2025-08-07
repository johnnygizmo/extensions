import bpy
from bpy.types import AddonPreferences, StringProperty

class JOHNNYGIZMO_FloorPlanner_Preferences(AddonPreferences):
    bl_idname = __package__

    # some_setting: StringProperty(
    #     name="Example Setting",
    #     description="This is just a placeholder",
    #     default=""
    # )

    def draw(self, context):
        layout = self.layout
        layout.label(text="My Addon Preferences")
        layout.operator("myaddon.copy_assets_to_user_library", icon="FILE_BLEND")

def register():
    bpy.utils.register_class(JOHNNYGIZMO_FloorPlanner_Preferences)


def unregister():
    bpy.utils.unregister_class(JOHNNYGIZMO_FloorPlanner_Preferences)