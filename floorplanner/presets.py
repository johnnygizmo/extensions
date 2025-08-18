import bpy
from bl_operators.presets import AddPresetBase
from os import path
from . import preferences

class JOHNNYGIZMO_FLOORPLANNER_MT_presets(bpy.types.Menu):
    bl_label = "Door Presets"
    preset_subdir = "johnnygizmo_floorplanner"+ path.sep +"doors"   # Folder inside scripts/presets/
    preset_operator = "script.execute_preset"
    def draw(self, context):
        layout = self.layout
        self.draw_preset(context)
        layout.separator()

        op = layout.operator("mesh.johnnygizmo_floorplanner_set_door_preset", text="Standard 80x36")
        op.width = 0.9144
        op.height=2.032

        op = layout.operator("mesh.johnnygizmo_floorplanner_set_door_preset", text="Standard 80x24")
        op.width = 0.6096
        op.height=2.032

        op = layout.operator("mesh.johnnygizmo_floorplanner_set_door_preset", text="Standard 80x28")
        op.width = 0.7112
        op.height=2.032

        op = layout.operator("mesh.johnnygizmo_floorplanner_set_door_preset", text="Standard 80x30")
        op.width = 0.762
        op.height=2.032

        op = layout.operator("mesh.johnnygizmo_floorplanner_set_door_preset", text="Standard 80x32")
        op.width = 0.8128
        op.height= 2.032

        op = layout.operator("mesh.johnnygizmo_floorplanner_set_door_preset", text="Sliding Door 80x60")
        op.width = 1.524
        op.height= 2.032

class MESH_OT_johnnygizmo_floorplanner_set_door_preset(bpy.types.Operator):
    """Set or create edge attribute with specified value for selected edges"""
    bl_idname = "mesh.johnnygizmo_floorplanner_set_door_preset"
    bl_label = "Set Door Attribute"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties    
    height: bpy.props.FloatProperty(
        name="Door Height"
    )# type: ignore
    
    width: bpy.props.FloatProperty(
        name="Door Width"
    )# type: ignore

    def execute(self, context):
        bpy.context.scene.johnnygizmo_floorplanner_tool_settings.door_height = self.height
        bpy.context.scene.johnnygizmo_floorplanner_tool_settings.door_width = self.width
        return {'FINISHED'}
    
class AddDoorPresetJohnnyGizmoFloorplanner(AddPresetBase, bpy.types.Operator):
    """Add a new MyAddon Preset"""
    bl_idname = "johnnygizmo_floorplanner.add_preset"
    bl_label = "Floor Planner Add Door Preset"
    preset_menu = "JOHNNYGIZMO_FLOORPLANNER_MT_door_presets"

    # The path where the preset files are saved
    preset_defines = [
        "mytool = bpy.context.scene.johnnygizmo_floorplanner_tool_settings"
    ]

    # Properties to store in each preset
    preset_values = [
        "mytool.door_width",
        "mytool.door_height"
    ]

    preset_subdir = "johnnygizmo_floorplanner"+ path.sep +"doors"


classes = (
    JOHNNYGIZMO_FLOORPLANNER_MT_presets,
    MESH_OT_johnnygizmo_floorplanner_set_door_preset,
    AddDoorPresetJohnnyGizmoFloorplanner
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
   

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()