import bpy  # type: ignore
import bmesh  # type: ignore
from mathutils import Vector # type: ignore

def get_bone_items(self, context):
    obj = context.object
    if obj and obj.parent and obj.parent.type == 'ARMATURE':
        armature = obj.parent.data
        return [
            (bone.name, bone.name, "")
            for bone in armature.bones
            if not self.limit_to_deform_bones or bone.use_deform
        ]
    return []

class MESH_OT_johnnygizmo_vertex_bone_picker(bpy.types.Operator):
    """Assign selected vertices to a bone's vertex group"""
    bl_idname = "mesh.johnnygizmo_vertex_bone_picker"
    bl_label = "Vertex Bone Assignment"
    bl_options = {'REGISTER', 'UNDO'}

    bone_name: bpy.props.EnumProperty(
        name="Pick Bone",
        description="Choose a bone to assign selected vertices to",
        items=get_bone_items
    )  # type: ignore

    replace_all: bpy.props.BoolProperty(
        name="Replace All Assignments",
        description="Clear all existing vertex group assignments for selected vertices before assigning to this bone",
        default=True
    )  # type: ignore

    limit_to_deform_bones: bpy.props.BoolProperty(
        name="Only Show Deform Bones",
        description="Limit bone list to deforming bones only",
        default=True
    )  # type: ignore

    _original_show_names = None
    _original_in_front = None

    def invoke(self, context, event):
        obj = context.object

        if obj is None or obj.type != 'MESH' or context.mode != 'EDIT_MESH':
            self.report({'ERROR'}, "Must be in mesh edit mode on a mesh object.")
            return {'CANCELLED'}

        bm = bmesh.from_edit_mesh(obj.data)
        selected_verts = [v for v in bm.verts if v.select]
        if not selected_verts:
            self.report({'ERROR'}, "No vertices selected.")
            return {'CANCELLED'}

        if obj.parent is None or obj.parent.type != 'ARMATURE':
            self.report({'ERROR'}, "Object must have an armature as a parent.")
            return {'CANCELLED'}

        armature_obj = obj.parent
        self._original_show_names = armature_obj.data.show_names
        self._original_in_front = armature_obj.show_in_front

        if not self._original_show_names:
            armature_obj.data.show_names = True
        if not self._original_in_front:
            armature_obj.show_in_front = True

        # Try to auto-assign closest bone
        self._auto_select_closest_bone(obj, selected_verts)

        return context.window_manager.invoke_props_dialog(self)

    def _auto_select_closest_bone(self, mesh_obj, selected_verts):
        armature_obj = mesh_obj.parent
        deform_only = self.limit_to_deform_bones

        world_matrix = mesh_obj.matrix_world
        avg_world_pos = sum((world_matrix @ v.co for v in selected_verts), Vector()) / len(selected_verts)

        min_dist = float('inf')
        closest_bone_name = None

        for bone in armature_obj.data.bones:
            if deform_only and not bone.use_deform:
                continue
            head_world = armature_obj.matrix_world @ bone.head_local
            tail_world = armature_obj.matrix_world @ bone.tail_local
            mid_point = (head_world + tail_world) / 2
            dist = (avg_world_pos - mid_point).length
            if dist < min_dist:
                min_dist = dist
                closest_bone_name = bone.name

        if closest_bone_name:
            self.bone_name = closest_bone_name


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "bone_name")
        layout.prop(self, "replace_all")
        layout.prop(self, "limit_to_deform_bones")

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

        if self.replace_all:
            for vg in obj.vertex_groups:
                vg.remove([v.index for v in selected_verts])

        vg = obj.vertex_groups.get(bone_name)
        if vg is None:
            vg = obj.vertex_groups.new(name=bone_name)

        for v in selected_verts:
            vg.add([v.index], 1.0, 'REPLACE')

        bpy.ops.object.mode_set(mode='EDIT')

        if self._original_show_names is not None:
            obj.parent.data.show_names = self._original_show_names
        if self._original_in_front is not None:
            obj.parent.show_in_front = self._original_in_front

        msg = f"Assigned {len(selected_verts)} vertices to '{bone_name}'"
        if self.replace_all:
            msg += " (replaced all previous assignments)"
        self.report({'INFO'}, msg)
        return {'FINISHED'}

    def cancel(self, context):
        obj = context.object
        if obj and obj.parent:
            if self._original_show_names is not None:
                obj.parent.data.show_names = self._original_show_names
            if self._original_in_front is not None:
                obj.parent.show_in_front = self._original_in_front

# Add to Vertex menu
def menu_func(self, context):
    self.layout.operator(MESH_OT_johnnygizmo_vertex_bone_picker.bl_idname, icon='BONE_DATA')

# Register
def register():
    bpy.utils.register_class(MESH_OT_johnnygizmo_vertex_bone_picker)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(menu_func)
    bpy.utils.unregister_class(MESH_OT_johnnygizmo_vertex_bone_picker)
