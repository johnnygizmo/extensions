import bpy # type: ignore
import bmesh # type: ignore
from mathutils import Vector # type: ignore

BONE_LOCATIONS = {}

def get_selected_vert_center(context):
    obj = context.edit_object
    bm = bmesh.from_edit_mesh(obj.data)
    selected_verts = [v.co for v in bm.verts if v.select]
    if not selected_verts:
        return None
    center = sum(selected_verts, Vector()) / len(selected_verts)
    return obj.matrix_world @ center

def get_bone_endpoints(self, context):
    global BONE_LOCATIONS
    bone_points = []
    center = get_selected_vert_center(context)
    obj = context.edit_object
    armature_obj = obj.parent

    BONE_LOCATIONS.clear()

    for bone in armature_obj.data.bones:
        head_label = f"{bone.name} >>> Head"
        tail_label = f"{bone.name} >>> Tail"

        head_loc = armature_obj.matrix_world @ bone.head_local
        tail_loc = armature_obj.matrix_world @ bone.tail_local

        BONE_LOCATIONS[head_label] = head_loc
        BONE_LOCATIONS[tail_label] = tail_loc

        bone_points.append((head_label, head_label, head_loc))
        bone_points.append((tail_label, tail_label, tail_loc))

    bone_points.sort(key=lambda x: (x[2] - center).length)
    return [(x[0], x[1], f"Distance: {(x[2] - center).length:.2f}") for x in bone_points]

class MESH_OT_johnnygizmo_mesh_bone_magnet_operator(bpy.types.Operator):
    bl_idname = "object.johnnygizmo_mesh_bone_magnet"
    bl_label = "Mesh Bone Magnet"
    bl_options = {'REGISTER', 'UNDO'}

    target_bone_part: bpy.props.EnumProperty(
        name="Target Bone Part",
        description="Choose a bone endpoint to move",
        items=get_bone_endpoints
    ) # type: ignore

    move_tail_with_head: bpy.props.BoolProperty(
        name="Move Tail With Head",
        description="If true, move the tail along with the head",
        default=False
    ) # type: ignore


    _show_names_prev: bool = False
    _show_in_front_prev: bool = False

    def invoke(self, context, event):
        obj = context.edit_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Not in mesh edit mode.")
            return {'CANCELLED'}

        if not obj.parent or obj.parent.type != 'ARMATURE':
            self.report({'ERROR'}, "Mesh must have an armature parent.")
            return {'CANCELLED'}

        if not get_selected_vert_center(context):
            self.report({'ERROR'}, "No selected vertices.")
            return {'CANCELLED'}

        

        armature = obj.parent
        self._show_names_prev = armature.data.show_names
        self._show_in_front_prev = armature.show_in_front

        armature.data.show_names = True
        armature.show_in_front = True

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        mesh_obj = context.edit_object
        arm_obj = mesh_obj.parent
        bone_name, part = self.target_bone_part.split(" >>> ")
        bpy.ops.view3d.snap_cursor_to_selected()
        
        bpy.ops.object.mode_set(mode='OBJECT')
        context.view_layer.objects.active = arm_obj
        bpy.ops.object.mode_set(mode='EDIT')

        bone = arm_obj.data.edit_bones.get(bone_name)
        if not bone:
            self.report({'ERROR'}, "Bone not found.")
            return {'CANCELLED'}

        
        cursor_world = context.scene.cursor.location
        cursor_local = arm_obj.matrix_world.inverted() @ cursor_world

        # if part == "Head":
        #     # Keep tail in world space
        #     world_tail = arm_obj.matrix_world @ bone.tail
        #     bone.head = cursor_local
        #     bone.tail = arm_obj.matrix_world.inverted() @ world_tail
        if part == "Head":
            if self.move_tail_with_head:
                # Move both head and tail, preserving bone vector
                delta = cursor_local - bone.head
                bone.head = cursor_local
                bone.tail += delta
            else:
                # Move just the head, preserve world-space tail
                world_tail = arm_obj.matrix_world @ bone.tail
                bone.head = cursor_local
                bone.tail = arm_obj.matrix_world.inverted() @ world_tail


        elif part == "Tail":
            bone.tail = cursor_local

        bpy.ops.object.mode_set(mode='OBJECT')
        context.view_layer.objects.active = mesh_obj
        bpy.ops.object.mode_set(mode='EDIT')

        # Restore armature visual settings
        arm_obj.data.show_names = self._show_names_prev
        arm_obj.show_in_front = self._show_in_front_prev

        return {'FINISHED'}

    def cancel(self, context):
        # Restore settings if dialog is cancelled
        obj = context.edit_object
        if obj and obj.parent and obj.parent.type == 'ARMATURE':
            arm = obj.parent
            arm.data.show_names = self._show_names_prev
            arm.show_in_front = self._show_in_front_prev

def menu_func(self, context):
    self.layout.operator(MESH_OT_johnnygizmo_mesh_bone_magnet_operator.bl_idname, icon='SNAP_ON')

def register():
    bpy.utils.register_class(MESH_OT_johnnygizmo_mesh_bone_magnet_operator)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_vertices.remove(menu_func)
    bpy.utils.unregister_class(MESH_OT_johnnygizmo_mesh_bone_magnet_operator)
    