import bpy# type: ignore
import bmesh# type: ignore
from bpy.props import FloatProperty, IntProperty, BoolProperty# type: ignore
from bpy.types import Operator# type: ignore

class MESH_OT_johnnygizmo_floorplanner_set_wall(Operator):
    """Set Wall Attribute"""
    bl_idname = "mesh.johnnygizmo_floorplanner_set_wall"
    bl_label = "Set Wall Attribute"
    bl_options = {'REGISTER', 'UNDO'}
    action: IntProperty(
        name="action", 
        description="",
        default=0
    )   # type: ignore
    # Properties
    hide: IntProperty(
        name="hide", 
        description="1 hide, 0 show",
        default=0
    ) # type: ignore

    width: FloatProperty(
        name="Width Override", 
        description="Override the wall width",
        default=0,
        subtype='DISTANCE'
    ) # type: ignore

    centering: FloatProperty(
        name="Centering Override", 
        description="Override the wall centering",
        default=0,
        subtype='DISTANCE'
    ) # type: ignore # 

    # Properties
    extend1: FloatProperty(
        name="Extend Start", 
        description="Start of the wall extension",
        default=0,
        subtype='DISTANCE'
    ) # type: ignore
    extend2: FloatProperty(
        name="Extend End", 
        description="End of the wall extension",
        default=0,
        subtype='DISTANCE'
    ) # type: ignore

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and 
                context.active_object.type == 'MESH' and
                context.mode == 'EDIT_MESH')
    
    def execute(self, context):

        if self.action == 1:
            bpy.ops.mesh.set_edge_int_attribute(
                'EXEC_DEFAULT',
                attr_name="wall_hide",
                attr_value=self.hide,
            )

            if self.hide == 0:
                bpy.ops.mesh.johnnygizmo_floorplanner_set_edge_float_attribute(
                    'EXEC_DEFAULT',
                    attr_name="door_height",
                    attr_value=0,
                )

                bpy.ops.mesh.johnnygizmo_floorplanner_set_edge_float_attribute(
                    'EXEC_DEFAULT',
                    attr_name="window_height",
                    attr_value=0,
                )

        else:
            bpy.ops.mesh.johnnygizmo_floorplanner_set_edge_float_attribute(
                'EXEC_DEFAULT',
                attr_name="wall_width",
                attr_value=self.width,
                
            )

            bpy.ops.mesh.johnnygizmo_floorplanner_set_edge_float_attribute(
                'EXEC_DEFAULT',
                attr_name="wall_extend1",
                attr_value=self.extend1,
            )

            bpy.ops.mesh.johnnygizmo_floorplanner_set_edge_float_attribute(
                'EXEC_DEFAULT',
                attr_name="wall_extend2",
                attr_value=self.extend2,
            )

            bpy.ops.mesh.johnnygizmo_floorplanner_set_edge_float_attribute(
                'EXEC_DEFAULT',
                attr_name="wall_center",
                attr_value=self.centering,
            )
        return {'FINISHED'}


class MESH_OT_johnnygizmo_floorplanner_set_wall_ext(Operator):
    """Set Wall Attribute"""
    bl_idname = "mesh.johnnygizmo_floorplanner_set_wall_ext"
    bl_label = "Set Wall Attribute"
    bl_options = {'REGISTER', 'UNDO'}
    
    value: BoolProperty(
        name="action", 
        description="",
        default=False
    )  # type: ignore

    # Properties
    end: IntProperty(
        name="End",
        description="",
        default=0
    ) # type: ignore


    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and 
                context.active_object.type == 'MESH' and
                context.mode == 'EDIT_MESH')
    
    def execute(self, context):

        if self.end == 1:
            bpy.ops.mesh.set_edge_bool_attribute(
                    'EXEC_DEFAULT',
                    attr_name="wall_extend1half",
                    attr_value=self.value,
            )
        else:
            bpy.ops.mesh.set_edge_bool_attribute(
                    'EXEC_DEFAULT',
                    attr_name="wall_extend2half",
                    attr_value=self.value,
            )
        return {'FINISHED'}



class MESH_OT_johnnygizmo_floorplanner_load_edge_averages(Operator):
    """Load Edge Averages"""
    bl_idname = "mesh.load_edge_averages"
    bl_label = "Load Edge Averages"
    bl_options = {'INTERNAL', 'UNDO'}
      
    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and 
                context.active_object.type == 'MESH' and
                context.mode == 'EDIT_MESH')
    
    def execute(self, context):
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        bm.edges.ensure_lookup_table()

        total = 0.0
        count = 0

        # Get the custom float layer for wall_width
        # wall_width
        layer_width = bm.edges.layers.float.get("wall_width")
        if layer_width is None:
            self.report({'WARNING'}, "No 'wall_width' attribute found on edges.")
            return {'CANCELLED'}

        # wall_extend1
        layer_extend1 = bm.edges.layers.float.get("wall_extend1")
        if layer_extend1 is None:
            self.report({'WARNING'}, "No 'wall_extend1' attribute found on edges.")
            return {'CANCELLED'}

        # wall_extend2
        layer_extend2 = bm.edges.layers.float.get("wall_extend2")
        if layer_extend2 is None:
            self.report({'WARNING'}, "No 'wall_extend2' attribute found on edges.")
            return {'CANCELLED'}

        # wall_center
        layer_center = bm.edges.layers.float.get("wall_center")
        if layer_center is None:
            self.report({'WARNING'}, "No 'wall_center' attribute found on edges.")
            return {'CANCELLED'}

        total_width = total_extend1 = total_extend2 = total_center = 0.0
        count = 0

        for edge in bm.edges:
            if edge.select:
                total_width += edge[layer_width]
                total_extend1 += edge[layer_extend1]
                total_extend2 += edge[layer_extend2]
                total_center += edge[layer_center]
                count += 1

        if count == 0:
            self.report({'WARNING'}, "No selected edges.")
            return {'CANCELLED'}

        context.scene.johnnygizmo_floorplanner_tool_settings.wall_width = total_width / count
        context.scene.johnnygizmo_floorplanner_tool_settings.wall_ext1 = total_extend1 / count
        context.scene.johnnygizmo_floorplanner_tool_settings.wall_ext2 = total_extend2 / count
        context.scene.johnnygizmo_floorplanner_tool_settings.wall_center = total_center / count

        return {'FINISHED'}



def register():
    bpy.utils.register_class(MESH_OT_johnnygizmo_floorplanner_set_wall)
    bpy.utils.register_class(MESH_OT_johnnygizmo_floorplanner_set_wall_ext)
    bpy.utils.register_class(MESH_OT_johnnygizmo_floorplanner_load_edge_averages)

def unregister():
    bpy.utils.unregister_class(MESH_OT_johnnygizmo_floorplanner_load_edge_averages)
    bpy.utils.unregister_class(MESH_OT_johnnygizmo_floorplanner_set_wall_ext)
    bpy.utils.unregister_class(MESH_OT_johnnygizmo_floorplanner_set_wall)
