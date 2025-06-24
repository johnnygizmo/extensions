import bpy
import bmesh
from mathutils import Vector

def get_selected_vert_center(obj):
    bm = bmesh.from_edit_mesh(obj.data)
    selected_verts = [v.co for v in bm.verts if v.select]
    if not selected_verts:
        return None
    center = sum(selected_verts, Vector()) / len(selected_verts)
    return obj.matrix_world @ center

def get_bone_endpoints(armature_obj):
    bone_points = []
    for bone in armature_obj.data.bones:
        print(f"Processing bone: {bone.name}")
        bone_points.append((f"{bone.name} - Head", armature_obj.matrix_world @ bone.head_local))
        bone_points.append((f"{bone.name} - Tail", armature_obj.matrix_world @ bone.tail_local))
    return bone_points
    
class BoneMagnetOperator(bpy.types.Operator):
    bl_idname = "object.bone_magnet"
    bl_label = "Mesh Bone Magnet"
    bl_options = {'REGISTER', 'UNDO'}

    target_bone_part: bpy.props.EnumProperty(
        name="Target Bone Part",
        description="Choose a bone endpoint to move",
        items=[]
    )

    def invoke(self, context, event):
        obj = context.edit_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Not in mesh edit mode.")
            return {'CANCELLED'}

        if not obj.parent or obj.parent.type != 'ARMATURE':
            self.report({'ERROR'}, "Mesh must have an armature parent.")
            return {'CANCELLED'}

        center = get_selected_vert_center(obj)
        if not center:
            self.report({'ERROR'}, "No selected vertices.")
            return {'CANCELLED'}

        bone_data = get_bone_endpoints(obj.parent)

        # Sort bone parts by distance to center
        sorted_bone_data = sorted(bone_data, key=lambda x: (x[1] - center).length)
        self._sorted_bone_map = sorted_bone_data  # Keep for execute()

        # Create dropdown items
        items = [(name, name, "") for name, _ in sorted_bone_data]
        self.__class__.target_bone_part = bpy.props.EnumProperty(
            name="Target Bone Part",
            description="Choose a bone endpoint to move",
            items=items
        )

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        mesh_obj = context.edit_object
        arm_obj = mesh_obj.parent
        bone_name, part = self.target_bone_part.split(" - ")

        # Snap cursor to selected
        bpy.ops.view3d.snap_cursor_to_selected()

        # Switch to armature edit mode
        bpy.ops.object.mode_set(mode='OBJECT')
        context.view_layer.objects.active = arm_obj
        bpy.ops.object.mode_set(mode='EDIT')

        bone = arm_obj.data.edit_bones.get(bone_name)
        if not bone:
            self.report({'ERROR'}, "Bone not found.")
            return {'CANCELLED'}

        cursor_loc = context.scene.cursor.location

        if part == "Head":
            offset = cursor_loc - bone.head
            bone.head = cursor_loc
            bone.tail += offset
        elif part == "Tail":
            bone.tail = cursor_loc

        # Restore mesh as active and back to edit mode
        bpy.ops.object.mode_set(mode='OBJECT')
        context.view_layer.objects.active = mesh_obj
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

def register():
    bpy.utils.register_class(BoneMagnetOperator)

def unregister():
    bpy.utils.unregister_class(BoneMagnetOperator)
