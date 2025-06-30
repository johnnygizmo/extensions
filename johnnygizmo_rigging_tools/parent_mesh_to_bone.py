import bpy  # type: ignore

class OBJECT_OT_johnnygizmo_parent_mesh_to_selected_bone(bpy.types.Operator):
    """Parent a mesh to a selected bone via popup"""
    bl_idname = "object.johnnygizmo_parent_mesh_to_selected_bone"
    bl_label = "Parent Mesh to Selected Bone"
    bl_options = {'REGISTER', 'UNDO'}

    _hold_names: False


    def invoke(self, context, event):
        self._hold_names = False
        props = context.scene.johnnygizmo_rigging_tools_properties
        selected = [obj for obj in context.selected_objects if obj.type == 'MESH']
        armature = [obj for obj in context.selected_objects if obj.type == 'ARMATURE']

        if len(selected) != 1:
            self.report({'ERROR'}, "Select exactly one mesh object")
            props.clear()
            return {'CANCELLED'}
       
        if armature and len(armature) == 1:
            if armature[0].data.show_names == False:
                self._hold_names = True
                armature[0].data.show_names = True

        props.selected_object_2 = selected[0]
        props.selected_object = armature[0] if armature else None

        # Try to prepopulate from existing parent
        if selected[0].parent and selected[0].parent_type == 'BONE':
            if selected[0].parent.type == 'ARMATURE':
                props.selected_bone = selected[0].parent_bone

        return context.window_manager.invoke_props_dialog(self, width=400)

    def cancel(self, context):
        props = context.scene.johnnygizmo_rigging_tools_properties
        armature = props.selected_object
        if self._hold_names and armature and armature.type == 'ARMATURE':
            armature.data.show_names = False
            self._hold_names = False
        props.clear()


    def draw(self, context):
        layout = self.layout
        props = context.scene.johnnygizmo_rigging_tools_properties

        layout.prop_search(props, "selected_object", context.scene, "objects", text="Parent")
        
        if props.selected_object and props.selected_object.type == 'ARMATURE':
            layout.prop_search(
                props, "selected_bone",
                props.selected_object.data, "bones",
                text="Bone"
            )

    def execute(self, context):
        props = context.scene.johnnygizmo_rigging_tools_properties
        armature = props.selected_object
        bone_name = props.selected_bone
        mesh = props.selected_object_2

        if not all([mesh, armature, bone_name]):
            if self._hold_names and armature:
                armature.data.show_names = False
                self._hold_names = False
            self.report({'ERROR'}, "Mesh, armature, and bone must all be selected")
            props.clear()

            return {'CANCELLED'}

        # Preserve world transform
        world_matrix = mesh.matrix_world.copy()

        mesh.parent = armature
        mesh.parent_type = 'BONE'
        mesh.parent_bone = bone_name
        mesh.matrix_world = world_matrix

        self.report({'INFO'}, f"Parented {props.selected_object_2.name} to {bone_name}")
        
        if self._hold_names and armature:
            armature.data.show_names = False

        props.clear()
        return {'FINISHED'}
    
    def cancel(self, context):
        props = context.scene.johnnygizmo_rigging_tools_properties
        props.clear()
        return {'CANCELLED'}    

def register(): 
    bpy.utils.register_class(OBJECT_OT_johnnygizmo_parent_mesh_to_selected_bone)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_johnnygizmo_parent_mesh_to_selected_bone)