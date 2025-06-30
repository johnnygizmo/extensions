import bpy # type: ignore # type: ignore
from mathutils import Vector # type: ignore

BONE_LOCATIONS = {}

def get_selected_joint_locations(context):
    obj = context.edit_object
    bones = obj.data.edit_bones
    locs = []

    for bone in bones:
        if bone.select_head:
            locs.append(obj.matrix_world @ bone.head)
        if bone.select_tail:
            locs.append(obj.matrix_world @ bone.tail)

    return locs

def get_bone_endpoints(self, context):
    global BONE_LOCATIONS
    bone_points = []
    center_list = get_selected_joint_locations(context)
    if not center_list:
        return []

    center = sum(center_list, Vector()) / len(center_list)
    obj = context.edit_object

    BONE_LOCATIONS.clear()

    for bone in obj.data.edit_bones:
        if bone.select:
            continue  # ignore any part of selected bone to avoid snapping to self

        head_label = f"{bone.name} >>> Head"
        tail_label = f"{bone.name} >>> Tail"

        head_loc = obj.matrix_world @ bone.head
        tail_loc = obj.matrix_world @ bone.tail

        BONE_LOCATIONS[head_label] = head_loc
        BONE_LOCATIONS[tail_label] = tail_loc

        dist_head = (head_loc - center).length
        dist_tail = (tail_loc - center).length


        if dist_head > 0.0:
            BONE_LOCATIONS[head_label] = head_loc
            bone_points.append((head_label, head_label, head_loc))

        if dist_tail > 0.0:
            BONE_LOCATIONS[tail_label] = tail_loc
            bone_points.append((tail_label, tail_label, tail_loc))

    bone_points.sort(key=lambda x: (x[2] - center).length)
    return [(x[0], x[1], f"Distance: {(x[2] - center).length:.2f}") for x in bone_points]

class ARMATURE_OT_johnnygizmo_armature_bone_magnet(bpy.types.Operator):
    bl_idname = "armature.johnnygizmo_armature_bone_magnet"
    bl_label = "Armature Bone Magnet"
    bl_options = {'REGISTER', 'UNDO'}

    target_bone_part: bpy.props.EnumProperty(
        name="Target Bone Part",
        description="Choose a bone part to snap",
        items=get_bone_endpoints
    ) # type: ignore


    move_tail_with_head: bpy.props.BoolProperty(
        name="Move Tail With Head",
        description="If true, move the tail when the head is moved",
        default=False
    ) # type: ignore

    _show_names_prev: bool = False
    _show_in_front_prev: bool = False

    def invoke(self, context, event):
        obj = context.edit_object
        if not obj or obj.type != 'ARMATURE' or context.mode != 'EDIT_ARMATURE':
            self.report({'ERROR'}, "Not in armature edit mode.")
            return {'CANCELLED'}

        if not get_selected_joint_locations(context):
            self.report({'ERROR'}, "No bone joints selected.")
            return {'CANCELLED'}

        bpy.ops.view3d.snap_cursor_to_selected()

        self._show_names_prev = obj.data.show_names
        self._show_in_front_prev = obj.show_in_front

        obj.data.show_names = True
        obj.show_in_front = True

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        obj = context.edit_object
        bones = obj.data.edit_bones
        bone_name, part = self.target_bone_part.split(" >>> ")

        target_pos = BONE_LOCATIONS.get(self.target_bone_part)
        if not target_pos:
            self.report({'ERROR'}, "Invalid target bone part.")
            return {'CANCELLED'}

        # Move the target bone part to each selected joint (averaged if multiple)
        selected_joints = get_selected_joint_locations(context)
        if not selected_joints:
            self.report({'ERROR'}, "No joints selected.")
            return {'CANCELLED'}

        average_loc = sum(selected_joints, Vector()) / len(selected_joints)
        local_target = obj.matrix_world.inverted() @ average_loc

        target_bone = bones.get(bone_name)
        if not target_bone:
            self.report({'ERROR'}, "Target bone not found.")
            return {'CANCELLED'}

        # if part == "Head":
        #     world_tail = obj.matrix_world @ target_bone.tail
        #     target_bone.head = local_target
        #     target_bone.tail = obj.matrix_world.inverted() @ world_tail
        if part == "Head":
            if self.move_tail_with_head:
                delta = local_target - target_bone.head
                target_bone.head = local_target
                target_bone.tail += delta
            else:
                world_tail = obj.matrix_world @ target_bone.tail
                target_bone.head = local_target
                target_bone.tail = obj.matrix_world.inverted() @ world_tail        
        
        elif part == "Tail":
            target_bone.tail = local_target

        obj.data.show_names = self._show_names_prev
        obj.show_in_front = self._show_in_front_prev

        return {'FINISHED'}

    def cancel(self, context):
        obj = context.edit_object
        if obj and obj.type == 'ARMATURE':
            obj.data.show_names = self._show_names_prev
            obj.show_in_front = self._show_in_front_prev

def menu_func(self, context):
    self.layout.operator(ARMATURE_OT_johnnygizmo_armature_bone_magnet.bl_idname, icon='SNAP_ON')

def register():
    bpy.utils.register_class(ARMATURE_OT_johnnygizmo_armature_bone_magnet)
    bpy.types.VIEW3D_MT_edit_armature.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_edit_armature.remove(menu_func)
    bpy.utils.unregister_class(ARMATURE_OT_johnnygizmo_armature_bone_magnet)
