import bpy# type: ignore
import bmesh# type: ignore
from bpy.props import FloatProperty, IntProperty# type: ignore
from bpy.types import Operator# type: ignore

class MESH_OT_johnnygizmo_floorplanner_set_baseboard(Operator):
    """Set Baseboard Attribute"""
    bl_idname = "mesh.set_baseboard"
    bl_label = "Set Baseboard Attribute"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties
    action : IntProperty(
        name="Action", 
        description="0 Side, 1 Cap",
        default=0
    ) # type: ignore

    side: IntProperty(
        name="Baseboard Side", 
        description="0 None, 1 Left, 2 Right, 3 Both",
        default=0
    ) # type: ignore

    cap: IntProperty(
        name="Baseboard Cap", 
        description="0 None, 1 Left, 2 Right, 3 Both",
        default=0
    ) # type: ignore

    extend: FloatProperty(
        name="Extend Length", 
        subtype='DISTANCE',
        description="Length to extend the baseboard",
        default=0
    ) # type: ignore    

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and 
                context.active_object.type == 'MESH' and
                context.mode == 'EDIT_MESH')
    
    def execute(self, context):
        if self.action == 0:
            bpy.ops.mesh.set_edge_int_attribute(
                'EXEC_DEFAULT',
                attr_name="baseboard_side",
                attr_value=self.side,
            )

        elif self.action == 1:
            bpy.ops.mesh.set_edge_int_attribute(
                'EXEC_DEFAULT',
                attr_name="baseboard_cap",
                attr_value=self.cap
            )      

        bpy.ops.mesh.set_edge_float_attribute(
            'EXEC_DEFAULT',
            attr_name="baseboard_extend",
            attr_value=self.extend,
        )

        return {'FINISHED'}
    
 

def register():
    bpy.utils.register_class(MESH_OT_johnnygizmo_floorplanner_set_baseboard)

def unregister():
    bpy.utils.unregister_class(MESH_OT_johnnygizmo_floorplanner_set_baseboard)
