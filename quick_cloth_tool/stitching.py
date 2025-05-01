import bpy # type: ignore

class QUICKCLOTH_OT_quick_cloth_stitch_edgeloops(bpy.types.Operator):
    """Applies a modifier named 'QuickCloth'."""
    bl_idname = "object.quick_cloth_stitch_edgeloops"
    bl_label = "Add Stiching Between Edge Loops"

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) != 0 and context.active_object.type == 'MESH'

    def execute(self, context):
        obj = context.active_object
        if obj and obj.type == 'MESH':
            bpy.ops.object.mode_set(mode='EDIT')   

            bpy.ops.mesh.bridge_edge_loops()
            bpy.ops.mesh.delete(type='ONLY_FACE')
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No object selected.")
            return {'CANCELLED'}     

class QUICKCLOTH_OT_quick_cloth_delete_loose_edges(bpy.types.Operator):
    """Delete loose edges"""
    bl_idname = "object.quick_cloth_delete_loose_edges"
    bl_label = "Delete Loose Edges"

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) != 0 and context.active_object.type == 'MESH'

    def execute(self, context):
        obj = context.active_object
        if obj:
            bpy.ops.object.mode_set(mode='EDIT')   
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
            bpy.ops.mesh.select_loose() 
            bpy.ops.mesh.delete(type='EDGE')
           
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No object selected.")
            return {'CANCELLED'}     


class QUICKCLOTH_OT_quick_cloth_stitch_vertring(bpy.types.Operator):
    """Applies a modifier named 'QuickCloth'."""
    bl_idname = "object.quick_cloth_stitch_vertring"
    bl_label = "Add Stiching Inside a Vertex Ring"
    bl_options = {'REGISTER', 'UNDO'}
    
    vertSkip: bpy.props.IntProperty(
        name="Vertices to Skip",
        description="Amount of vertices to skip when stitching",
        min=1,
        default=3
    ) # type: ignore

    offset: bpy.props.IntProperty(
        name="Vertex Offset",
        description="Offset for the stitching",
        min=0,
        default=0
    ) # type: ignore

    extrudeControl: bpy.props.BoolProperty(
        name="Extrude Control Ring",
        description="Extrude the control ring",
        default=True
    ) # type: ignore

    extrudeControlDistance: bpy.props.FloatProperty(
        name="Extrude Control Ring Distance",
        description="Distance to extrude the control ring",
        default=.2
    ) # type: ignore

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) != 0 and context.active_object.type == 'MESH'

    def execute(self, context):
        obj = context.active_object
        if obj:
            bpy.ops.object.mode_set(mode='EDIT')   
            bpy.ops.mesh.select_nth(skip=self.vertSkip, offset=self.offset)
            bpy.ops.mesh.edge_face_add()     
            if self.extrudeControl:
                bpy.ops.mesh.extrude_region_shrink_fatten(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_shrink_fatten={"value":self.extrudeControlDistance, "use_even_offset":False, "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":0.385543, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "release_confirm":True, "use_accurate":False})
                bpy.ops.mesh.select_more()  
            bpy.ops.mesh.delete(type='ONLY_FACE')
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No object selected.")
            return {'CANCELLED'}              



def register():
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_stitch_edgeloops)
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_stitch_vertring)
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_delete_loose_edges)

def unregister():
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_stitch_vertring)
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_stitch_edgeloops)
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_delete_loose_edges)
    