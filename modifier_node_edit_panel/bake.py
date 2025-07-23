import bpy

class JOHNNYGIZMO_OT_bake_geometry_node(bpy.types.Operator):
    bl_idname = "object.johnnygizmo_geometry_node_bake"
    bl_label = "Bake Geometry Nodes"
    bl_description = "Bake specific Geometry Nodes modifier"
    bl_options = {'REGISTER', 'UNDO'}
    
    action: bpy.props.IntProperty(
        name="Action",
        description="1-Bake, 0-Delete",
        default=0
    )
    session_uid: bpy.props.IntProperty(
        name="Session UID",
        description="Unique session ID for the bake operation",
        default=0
    )

    modifier_name: bpy.props.StringProperty(
        name="Modifier Name",
        description="Name of the Geometry Nodes modifier",
        default="GeometryNodes"
    )

    bake_id: bpy.props.IntProperty(
        name="Bake ID",
        description="Bake identifier from the Bake node",
        default=0
    )


    def execute(self, context):
        if self.action == 0:
            try:
                bpy.ops.object.geometry_node_bake_delete_single(
                    session_uid=self.session_uid,
                    modifier_name=self.modifier_name,
                    bake_id=self.bake_id
                )
                self.report({'INFO'}, "Bake deleted successfully.")
            except Exception as e:
                self.report({'ERROR'}, f"Bake deletion failed: {e}")
            return {'FINISHED'}
        else:
            try:
                bpy.ops.object.geometry_node_bake_single(
                    session_uid=self.session_uid,
                    modifier_name=self.modifier_name,
                    bake_id=self.bake_id
                )
                self.report({'INFO'}, "Bake triggered successfully.")
            except Exception as e:
                self.report({'ERROR'}, f"Bake failed: {e}")
            return {'FINISHED'}

def register():
    bpy.utils.register_class(JOHNNYGIZMO_OT_bake_geometry_node)

def unregister():
    bpy.utils.unregister_class(JOHNNYGIZMO_OT_bake_geometry_node)