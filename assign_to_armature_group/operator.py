import bpy # type: ignore
import bmesh # type: ignore

def get_bone_items(self, context):
    obj = context.object
    if obj and obj.parent and obj.parent.type == 'ARMATURE':
        return [(bone.name, bone.name, "") for bone in obj.parent.data.bones]
    return []

class MESH_OT_vertex_bone_picker(bpy.types.Operator):
    """Assign selected vertices to a bone's vertex group"""
    bl_idname = "mesh.vertex_bone_picker"
    bl_label = "Vertex Bone Picker"
    bl_options = {'REGISTER', 'UNDO'}

    bone_name: bpy.props.EnumProperty(
        name="Pick Bone",
        description="Choose a bone to assign selected vertices to",
        items=get_bone_items
    ) # type: ignore

    _original_show_names = None  

    def invoke(self, context, event):
        obj = context.object

        if obj is None or obj.type != 'MESH' or context.mode != 'EDIT_MESH':
            self.report({'ERROR'}, "Must be in mesh edit mode on a mesh object.")
            return {'CANCELLED'}

        bm = bmesh.from_edit_mesh(obj.data)
        if not any(v.select for v in bm.verts):
            self.report({'ERROR'}, "No vertices selected.")
            return {'CANCELLED'}

        if obj.parent is None or obj.parent.type != 'ARMATURE':
            self.report({'ERROR'}, "Object must have an armature as a parent.")
            return {'CANCELLED'}

        armature_obj = obj.parent
        armature_data = armature_obj.data

        self._original_show_names = armature_data.show_names
        if not self._original_show_names:
            armature_data.show_names = True

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        obj = context.object
        bone_name = self.bone_name

        if not bone_name:
            self.report({'ERROR'}, "No bone selected.")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='OBJECT')

        mesh = obj.data
        selected_verts = [v for v in mesh.vertices if v.select]
        if not selected_verts:
            self.report({'ERROR'}, "No vertices selected.")
            bpy.ops.object.mode_set(mode='EDIT')
            return {'CANCELLED'}

        vg = obj.vertex_groups.get(bone_name)
        if vg is None:
            vg = obj.vertex_groups.new(name=bone_name)

        for v in selected_verts:
            vg.add([v.index], 1.0, 'REPLACE')

        bpy.ops.object.mode_set(mode='EDIT')

        armature_obj = obj.parent
        if self._original_show_names is not None:
            armature_obj.data.show_names = self._original_show_names

        self.report({'INFO'}, f"Assigned {len(selected_verts)} vertices to '{bone_name}'")
        return {'FINISHED'}

    def cancel(self, context):
        obj = context.object
        if obj and obj.parent and self._original_show_names is not None:
            obj.parent.data.show_names = self._original_show_names


def register():
    bpy.utils.register_class(MESH_OT_vertex_bone_picker)

def unregister():
    bpy.utils.unregister_class(MESH_OT_vertex_bone_picker)

if __name__ == "__main__":
    register()
 # type: ignore