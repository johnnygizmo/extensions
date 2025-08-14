import bpy

class JOHNNYGIZMO_GEOMETRY_NODES_PT_exec_python_panel(bpy.types.Panel):
    """Run a script from Geometry Nodes"""
    bl_label = "Execute Python"
    bl_idname = "JOHNNYGIZMO_GEOMETRY_NODES_PT_exec_python_panel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Node"
    
    @classmethod
    def poll(cls, context):
        node_editor = context.space_data
        
        if not isinstance(node_editor, bpy.types.SpaceNodeEditor):
            return False        
        if not node_editor.node_tree:
            return False
        if not node_editor.node_tree.nodes:
            return False
        
        selected_nodes = node_editor.node_tree.nodes.active
        
        return (selected_nodes and 
                selected_nodes.bl_idname == 'NodeFrame' and 
                selected_nodes.label)

    def draw(self, context):
        layout = self.layout
        selected_frame = context.space_data.node_tree.nodes.active

        if selected_frame and selected_frame.text:            
            row = layout.row()
            row.label(text=f"Script: {selected_frame.text.name}")
            row = layout.row()
            row.operator("text.run_script_from_frame_node_frame", text="Run Script", icon='PLAY')

class JOHNNYGIZMO_ExecuteTextblockOperator(bpy.types.Operator):
    """Run the selected text block as a Python script"""
    bl_idname = "text.run_script_from_frame_node_frame"
    bl_label = "Run Script"
    
    def execute(self, context):
        node_editor = context.space_data
        selected_frame = node_editor.node_tree.nodes.active
        
        if selected_frame and selected_frame.text:
            text_block = selected_frame.text
            with context.temp_override(
                edit_text=text_block,
                area=context.area,
                region=context.region,
                space_data=context.space_data
            ):
                bpy.ops.text.run_script()
                self.report({'INFO'}, f"Script '{text_block.name}' executed successfully.")
        else:
            self.report({'WARNING'}, "No text block selected on the frame node.")
            
        return {'FINISHED'}


def register():
    bpy.utils.register_class(JOHNNYGIZMO_GEOMETRY_NODES_PT_exec_python_panel)
    bpy.utils.register_class(JOHNNYGIZMO_ExecuteTextblockOperator)

def unregister():
    bpy.utils.unregister_class(JOHNNYGIZMO_GEOMETRY_NODES_PT_exec_python_panel)
    bpy.utils.unregister_class(JOHNNYGIZMO_ExecuteTextblockOperator)

if __name__ == "__main__":
    register()