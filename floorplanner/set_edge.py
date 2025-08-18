import bpy # type: ignore
import bmesh # type: ignore
from bpy.props import StringProperty, FloatProperty,IntProperty, BoolProperty # type: ignore
from bpy.types import Operator # type: ignore

class MESH_OT_johnnygizmo_floorplanner_set_edge_float_attribute(Operator):
    """Set or create edge attribute with specified value for selected edges"""
    bl_idname = "mesh.johnnygizmo_floorplanner_set_edge_float_attribute"
    bl_label = "Set Edge Attribute"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties
    attr_name: StringProperty(
        name="Attribute Name",
        description="Name of the edge attribute to create/modify",
        default="custom_attr"
    ) # type: ignore
    
    attr_value: FloatProperty(
        name="Attribute Value", 
        description="Value to assign to the attribute",
        default=1.0
    )# type: ignore
    
    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and 
                context.active_object.type == 'MESH' and
                context.mode == 'EDIT_MESH')
    
    def execute(self, context):
        obj = context.active_object
        mesh = obj.data
        bm = bmesh.from_edit_mesh(mesh)
        layer = bm.edges.layers.float.get(self.attr_name)
        if layer is None:
            layer = bm.edges.layers.float.new(self.attr_name)
        for edge in bm.edges:
            if edge.select:
                edge[layer] = self.attr_value
        bmesh.update_edit_mesh(mesh, loop_triangles=False)
        
        return {'FINISHED'}





class MESH_OT_johnnygizmo_floorplanner_set_edge_bool_attribute(Operator):
    """Set or create edge attribute with specified value for selected edges"""
    bl_idname = "mesh.set_edge_bool_attribute"
    bl_label = "Set Edge Attribute"
    bl_options = {'REGISTER', 'UNDO'}

    # Properties
    attr_name: StringProperty(
        name="Attribute Name",
        description="Name of the edge attribute to create/modify",
        default="custom_attr"
    ) # type: ignore

    attr_value: BoolProperty(
        name="Attribute Value",
        description="Value to assign to the attribute",
        default=True
    ) # type: ignore

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and
                context.active_object.type == 'MESH' and
                context.mode == 'EDIT_MESH')

    def execute(self, context):
        obj = context.active_object
        mesh = obj.data
        bm = bmesh.from_edit_mesh(mesh)
        layer = bm.edges.layers.bool.get(self.attr_name)
        if layer is None:
            layer = bm.edges.layers.bool.new(self.attr_name)
        for edge in bm.edges:
            if edge.select:
                edge[layer] = self.attr_value
        bmesh.update_edit_mesh(mesh, loop_triangles=False)
        return {'FINISHED'}

    
   


class MESH_OT_johnnygizmo_floorplanner_set_edge_int_attribute(Operator):
    """Set or create edge attribute with specified value for selected edges"""
    bl_idname = "mesh.set_edge_int_attribute"
    bl_label = "Set Edge Attribute"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties
    attr_name: StringProperty(
        name="Attribute Name",
        description="Name of the edge attribute to create/modify",
        default="custom_attr"
    ) # type: ignore
    
    attr_value: IntProperty(
        name="Attribute Value", 
        description="Value to assign to the attribute",
        default=1
    )# type: ignore
    
    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and 
                context.active_object.type == 'MESH' and
                context.mode == 'EDIT_MESH')
    
    def execute(self, context):
        obj = context.active_object
        mesh = obj.data
        bm = bmesh.from_edit_mesh(mesh)
        layer = bm.edges.layers.int.get(self.attr_name)
        if layer is None:
            layer = bm.edges.layers.int.new(self.attr_name)
        for edge in bm.edges:
            if edge.select:
                edge[layer] = self.attr_value
        bmesh.update_edit_mesh(mesh, loop_triangles=False)
        
        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(MESH_OT_johnnygizmo_floorplanner_set_edge_float_attribute)
    bpy.utils.register_class(MESH_OT_johnnygizmo_floorplanner_set_edge_bool_attribute)
    bpy.utils.register_class(MESH_OT_johnnygizmo_floorplanner_set_edge_int_attribute)


def unregister():
    bpy.utils.unregister_class(MESH_OT_johnnygizmo_floorplanner_set_edge_float_attribute)
    bpy.utils.unregister_class(MESH_OT_johnnygizmo_floorplanner_set_edge_bool_attribute)
    bpy.utils.unregister_class(MESH_OT_johnnygizmo_floorplanner_set_edge_int_attribute)
