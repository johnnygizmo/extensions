import bpy# type: ignore
import bmesh# type: ignore
from bpy.props import IntProperty, FloatProperty# type: ignore
from bpy.types import Operator# type: ignore

class MESH_OT_johnnygizmo_floorplanner_set_window(Operator):
    """Set or create edge attribute with specified value for selected edges"""
    bl_idname = "mesh.set_window"
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
        bpy.ops.mesh.set_edge_float_attribute(
            'EXEC_DEFAULT',
            attr_name="window_height",
            attr_value=self.height,
        )


        bpy.ops.mesh.set_edge_float_attribute(
            'EXEC_DEFAULT',
            attr_name="window_width",
            attr_value=self.width,
        )
        bpy.ops.mesh.set_edge_float_attribute(
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
            
            bpy.ops.mesh.set_edge_float_attribute(
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
    
    # def invoke(self, context, event):
    #     # Show dialog for user input
    #     return context.window_manager.invoke_props_dialog(self)

def register():
    bpy.utils.register_class(MESH_OT_johnnygizmo_floorplanner_set_window)

def unregister():
    bpy.utils.unregister_class(MESH_OT_johnnygizmo_floorplanner_set_window)
