import bpy

class OBJECT_OT_johnnygizmo_bake_shape_keys_to_gn(bpy.types.Operator):
    bl_idname = "object.bake_shape_keys_to_gn"
    bl_label = "Bake Shape Keys to Geometry Nodes"
    bl_description = "Bakes each shape key using a Bake node in the Geometry Nodes modifier"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if not (obj and obj.type == 'MESH' and obj.data.shape_keys):
            return False

        # Check for a Geometry Nodes modifier with a node group
        for mod in obj.modifiers:
            if mod.type == 'NODES' and mod.node_group:
                return True

        return False

    def execute(self, context):
        obj = context.active_object
        if not obj or not obj.data.shape_keys:
            self.report({'ERROR'}, "Active object has no shape keys.")
            return {'CANCELLED'}

        shape_keys = obj.data.shape_keys.key_blocks
        gn_mod = next((mod for mod in obj.modifiers if mod.type == 'NODES'), None)
        if not gn_mod:
            self.report({'ERROR'}, "No Geometry Nodes modifier found.")
            return {'CANCELLED'}

        node_group = gn_mod.node_group
        if not node_group:
            self.report({'ERROR'}, "Geometry Nodes modifier has no node group.")
            return {'CANCELLED'}

        input_node = next((n for n in node_group.nodes if n.bl_idname == 'NodeGroupInput'), None)
        if not input_node:
            self.report({'ERROR'}, "No Group Input node found in the node group.")
            return {'CANCELLED'}

        geometry_output = next((o for o in input_node.outputs if o.name == "Geometry"), None)
        if not geometry_output:
            self.report({'ERROR'}, "No Geometry output on Group Input node.")
            return {'CANCELLED'}

        # Save original shape key values
        original_values = {k.name: k.value for k in shape_keys}

        offset = 0

        for key in shape_keys:

            # Reset all shape keys to 0, set this one to 1
            for k in shape_keys:
                k.value = 0.0
            
            if key.name != "Basis":
                key.value = 1.0
            bpy.context.view_layer.update()

            # Look for or create bake node
            bake_node = next((n for n in node_group.nodes
                              if n.bl_idname == 'GeometryNodeBake' and n.name == key.name), None)

            if not bake_node:
                bake_node = node_group.nodes.new("GeometryNodeBake")
                bake_node.name = key.name
                bake_node.label = key.name
                bake_node.location = (input_node.location.x + 300, input_node.location.y    + offset * -150)
                offset += 1
                node_group.links.new(geometry_output, bake_node.inputs['Geometry'])

            # Find bake entry for this node
            bake_entry = next((b for b in gn_mod.bakes if b.node == bake_node), None)
            if not bake_entry:
                self.report({'WARNING'}, f"No bake entry found for node '{key.name}', skipping.")
                continue

            try:
                bpy.ops.object.geometry_node_bake_single(
                    session_uid=obj.session_uid,
                    modifier_name=gn_mod.name,
                    bake_id=bake_entry.bake_id
                )
            except Exception as e:
                self.report({'WARNING'}, f"Failed to bake '{key.name}': {e}")
                continue

            # Reset the shape key again just in case
            key.value = 0.0

        # Restore original shape key values
        for key_name, val in original_values.items():
            shape_keys[key_name].value = val

        self.report({'INFO'}, "All shape keys baked.")
        return {'FINISHED'}





def menu_draw(self, context):
    if context.space_data.tree_type == 'GeometryNodeTree':
        self.layout.operator(OBJECT_OT_johnnygizmo_bake_shape_keys_to_gn.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_OT_johnnygizmo_bake_shape_keys_to_gn)
    bpy.types.NODE_MT_node.append(menu_draw)


def unregister():
    bpy.types.NODE_MT_node.remove(menu_draw)
    bpy.utils.unregister_class(OBJECT_OT_johnnygizmo_bake_shape_keys_to_gn)
