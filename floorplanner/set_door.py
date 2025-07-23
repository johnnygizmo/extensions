import bpy# type: ignore
import bmesh# type: ignore
from bpy.props import StringProperty, FloatProperty# type: ignore
from bpy.types import Operator# type: ignore

class MESH_OT_johnnygizmo_floorplanner_set_door(Operator):
    """Set or create edge attribute with specified value for selected edges"""
    bl_idname = "mesh.set_door"
    bl_label = "Set Door Attribute"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties    
    height: FloatProperty(
        name="door Height",
        subtype='DISTANCE',
        description="Height of the door above the base",
        default=5.0
    )# type: ignore
    
    # width: FloatProperty(
    #     name="door Width",
    #     description="Width of the door",
    #     subtype='DISTANCE',
    #     default=24.0
    # )# type: ignore

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and 
                context.active_object.type == 'MESH' and
                context.mode == 'EDIT_MESH')
    
    def execute(self, context):
        bpy.ops.mesh.set_edge_float_attribute(
            'EXEC_DEFAULT',
            attr_name="door_height",
            attr_value=self.height,
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
            
            bpy.ops.mesh.set_edge_float_attribute(
                'EXEC_DEFAULT',
                attr_name="window_height",
                attr_value=0,
            )



        return {'FINISHED'}
    
    # def invoke(self, context, event):
    #     return context.door_manager.invoke_props_dialog(self)

def register():
    bpy.utils.register_class(MESH_OT_johnnygizmo_floorplanner_set_door)

def unregister():
    bpy.utils.unregister_class(MESH_OT_johnnygizmo_floorplanner_set_door)
