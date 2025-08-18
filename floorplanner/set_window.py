import bpy# type: ignore
import bmesh# type: ignore
from bpy.props import IntProperty, FloatProperty# type: ignore
from bpy.types import Operator# type: ignore
from bl_operators.presets import AddPresetBase
from os import path
from . import preferences

class MESH_OT_johnnygizmo_floorplanner_set_window(Operator):
    """Set or create edge attribute with specified value for selected edges"""
    bl_idname = "mesh.johnnygizmo_floorplanner_set_window"
    bl_label = "Set Window Attribute"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties
    base: FloatProperty(
        name="Base Z Height", 
        description="Base Z height of the window",
        subtype='DISTANCE',
        default=2.0
    ) # type: ignore
    
    height: FloatProperty(
        name="Window Height",
        description="Height of the window above the base",
        subtype='DISTANCE',
        default=5.0
    )# type: ignore
    
    width: FloatProperty(
        name="Window Width",
        description="Width of the window",
        subtype='DISTANCE',
        default=24.0
    )# type: ignore

    index: IntProperty(
        name="Window Index",
        description="Index of the window",
        default=0
    )# type: ignore


    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and 
                context.active_object.type == 'MESH' and
                context.mode == 'EDIT_MESH')
    
    def execute(self, context):
        bpy.ops.jm_floorplanner.set_edge_length(
            'EXEC_DEFAULT',
            length=self.width,
        )


        bpy.ops.mesh.johnnygizmo_floorplanner_set_edge_float_attribute(
            'EXEC_DEFAULT',
            attr_name="window_height",
            attr_value=self.height,
        )



        bpy.ops.mesh.johnnygizmo_floorplanner_set_edge_float_attribute(
            'EXEC_DEFAULT',
            attr_name="window_width",
            attr_value=self.width,
        )
        bpy.ops.mesh.johnnygizmo_floorplanner_set_edge_float_attribute(
            'EXEC_DEFAULT',
            attr_name="window_base",
            attr_value=self.base,
        )
        bpy.ops.mesh.set_edge_int_attribute(
            'EXEC_DEFAULT',
            attr_name="window_index",
            attr_value=self.index,
        )

        if self.height > 0:
            bpy.ops.mesh.set_edge_int_attribute(
                'EXEC_DEFAULT',
                attr_name="wall_hide",
                attr_value=1,
            )
            
            bpy.ops.mesh.johnnygizmo_floorplanner_set_edge_float_attribute(
                'EXEC_DEFAULT',
                attr_name="door_height",
                attr_value=0,
            )
        else:
            bpy.ops.mesh.set_edge_int_attribute(
                'EXEC_DEFAULT',
                attr_name="wall_hide",
                attr_value=0,
            )
            
        
        return {'FINISHED'}
    


def window_preset(width,height,prefix,layout):
    h = round(height * 39.3701, 1)
    w = round(width * 39.3701, 1)
    text = f"{prefix} {w:.2g}\"x{h:.2g}\" ({width:.2f}m x {height:.2f}m)"
    op = layout.operator("mesh.johnnygizmo_floorplanner_set_window_preset", text=text)
    op.width  = width
    op.height = height  
    return op

class JOHNNYGIZMO_FLOORPLANNER_MT_window_presets(bpy.types.Menu):
    bl_label = "Window Presets"
    preset_subdir = "johnnygizmo_floorplanner"+ path.sep +"windows"   # Folder inside scripts/presets/
    preset_operator = "script.execute_preset"
    def draw(self, context):
        layout = self.layout
        self.draw_preset(context)
        layout.separator()

        window_preset(0.9144, 0.6096, "Picture (3020)", layout)
        window_preset(1.524, 0.9144, "Picture (5030)", layout)
        window_preset(1.8288, 1.2192, "Picture (6040)", layout)
        window_preset(1.2192, 1.524, "Picture (4050)", layout)


        window_preset(0.6096, 0.9144, "Single/Double Hung (2030)", layout)
        window_preset(0.6096, 1.3208, "Single/Double Hung (2044)", layout)
        window_preset(0.8128, 1.2192, "Single/Double Hung (2840)", layout)
        window_preset(0.8128, 0.6096, "Single/Double Hung (2852)", layout)

        window_preset(0.7112, 1.0668, "Casement (2436)", layout)
        window_preset(0.762, 1.2192, "Casement (2640)", layout)
        window_preset(0.8128, 1.524, "Casement (2850)", layout)
        window_preset( 0.9144, 1.8288, "Casement (3060)", layout)

        window_preset( 0.9144, 0.6096, "Awning (3020)", layout)
        window_preset( 1.2192, 0.7112, "Awning (4024)", layout)
        window_preset( 1.524, 0.9144, "Awning (5030)", layout)

        window_preset( 0.9144, 0.6096, "Sliding (3020)", layout)
        window_preset( 0.9144, 0.9144, "Sliding (3030)", layout)
        window_preset( 1.524,  0.9144, "Sliding (5030)", layout)
        window_preset( 1.8288, 1.2192, "Sliding (6040)", layout)


class MESH_OT_johnnygizmo_floorplanner_set_window_preset(bpy.types.Operator):
    """Set or create edge attribute with specified value for selected edges"""
    bl_idname = "mesh.johnnygizmo_floorplanner_set_window_preset"
    bl_label = "Set Window Attribute"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties    
    height: bpy.props.FloatProperty(
        name="Window Height"
    )# type: ignore
    
    width: bpy.props.FloatProperty(
        name="Window Width"
    )# type: ignore

    def execute(self, context):
        bpy.context.scene.johnnygizmo_floorplanner_tool_settings.window_height = self.height
        bpy.context.scene.johnnygizmo_floorplanner_tool_settings.window_width = self.width
        return {'FINISHED'}
    
class AddWindowPresetJohnnyGizmoFloorplanner(AddPresetBase, bpy.types.Operator):
    """Add a new MyAddon Preset"""
    bl_idname = "johnnygizmo_floorplanner.add_window_preset"
    bl_label = "Floor Planner Add Window Preset"
    preset_menu = "JOHNNYGIZMO_FLOORPLANNER_MT_window_presets"

    # The path where the preset files are saved
    preset_defines = [
        "mytool = bpy.context.scene.johnnygizmo_floorplanner_tool_settings"
    ]

    # Properties to store in each preset
    preset_values = [
        "mytool.window_width",
        "mytool.window_height"
    ]

    preset_subdir = "johnnygizmo_floorplanner"+ path.sep +"windows"


classes = (
    MESH_OT_johnnygizmo_floorplanner_set_window,
    JOHNNYGIZMO_FLOORPLANNER_MT_window_presets,
    MESH_OT_johnnygizmo_floorplanner_set_window_preset,
    AddWindowPresetJohnnyGizmoFloorplanner
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
   

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
