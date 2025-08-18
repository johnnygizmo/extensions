import bpy# type: ignore
import bmesh# type: ignore
from bpy.props import StringProperty, FloatProperty# type: ignore
from bpy.types import Operator# type: ignore
from bl_operators.presets import AddPresetBase
from os import path
from . import preferences


class MESH_OT_johnnygizmo_floorplanner_set_door(Operator):
    """Set or create edge attribute with specified value for selected edges"""
    bl_idname = "mesh.johnnygizmo_floorplanner_set_door"
    bl_label = "Set Door Attribute"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties    
    height: FloatProperty(
        name="Door Height",
        subtype='DISTANCE',
        description="Height of the door above the base",
        default=2
    )# type: ignore
    
    width: FloatProperty(
        name="Door Width",
        description="Width of the door",
        subtype='DISTANCE',
        default=0.8128
    )# type: ignore

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and 
                context.active_object.type == 'MESH' and
                context.mode == 'EDIT_MESH')
    
    def execute(self, context):
        bpy.ops.mesh.johnnygizmo_floorplanner_set_edge_float_attribute(
            'EXEC_DEFAULT',
            attr_name="door_height",
            attr_value=self.height,
        )

        bpy.ops.jm_floorplanner.set_edge_length(
            'EXEC_DEFAULT',
            length=self.width,
        )

        if self.height == 0:
            bpy.ops.mesh.set_edge_int_attribute(
                'EXEC_DEFAULT',
                attr_name="wall_hide",
                attr_value=0,
            )
        else:
            bpy.ops.mesh.set_edge_int_attribute(
                'EXEC_DEFAULT',
                attr_name="wall_hide",
                attr_value=1,
            )
            
            bpy.ops.mesh.johnnygizmo_floorplanner_set_edge_float_attribute(
                'EXEC_DEFAULT',
                attr_name="window_height",
                attr_value=0,
            )



        return {'FINISHED'}
    
    # def invoke(self, context, event):
    #     return context.door_manager.invoke_props_dialog(self)

def door_preset(width,height,prefix,layout):
    h = round(height * 39.3701, 1)
    w = round(width * 39.3701, 1)
    text = f"{prefix} {w:.2g}\"x{h:.2g}\" ({width:.2f}m x {height:.2f}m)"
    op = layout.operator("mesh.johnnygizmo_floorplanner_set_door_preset", text=text)
    op.width  = width
    op.height = height  
    return op

class JOHNNYGIZMO_FLOORPLANNER_MT_door_presets(bpy.types.Menu):
    bl_label = "Door Presets"
    preset_subdir = "johnnygizmo_floorplanner"+ path.sep +"doors"   # Folder inside scripts/presets/
    preset_operator = "script.execute_preset"
    def draw(self, context):
        layout = self.layout
        self.draw_preset(context)
        layout.separator()

        door_preset(0.9144, 2.032, "Standard", layout)
        door_preset(0.6096, 2.032, "Standard", layout)
        door_preset(0.7112, 2.032, "Standard", layout)
        door_preset(0.762, 2.032, "Standard", layout)
        door_preset(0.8128, 2.032, "Standard", layout)
        door_preset(1.524, 2.032, "Sliding", layout)

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
    bl_idname = "johnnygizmo_floorplanner.add_door_preset"
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
    MESH_OT_johnnygizmo_floorplanner_set_door,
    JOHNNYGIZMO_FLOORPLANNER_MT_door_presets,
    MESH_OT_johnnygizmo_floorplanner_set_door_preset,
    AddDoorPresetJohnnyGizmoFloorplanner
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
   

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
