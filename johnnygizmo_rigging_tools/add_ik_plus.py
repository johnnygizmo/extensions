import bpy
from bpy.types import Operator
from bpy.props import (
    EnumProperty,
    IntProperty,
    FloatProperty,
    BoolProperty,
    StringProperty
)


def get_pole_target_items(self, context):
    pose_bones = context.active_object.pose.bones
    selected_bones = [b.name for b in context.selected_pose_bones]
    items = [(b.name, b.name, "") for b in pose_bones if b.name not in selected_bones]
    if not items:
        items.append(('NONE', 'None Available', ''))
    else:
        items.insert(0,('NONE', 'No Pole Target', '')) 
    return items


class MESH_OT_johnnygizmo_ik_plus(Operator):
    bl_idname = "armature.johnnygizmo_add_ik_plus"
    bl_label = "Add IK Chain with Settings"
    bl_description = "Adds an IK constraint to the selected bones"
    bl_options = {'REGISTER', 'UNDO'}

    chain_length: IntProperty(name="Chain Length", default=2, min=0) # type: ignore
    iterations: IntProperty(name="Iterations", default=500, min=1) # type: ignore
    use_tail: BoolProperty(name="Use Tail", default=True) # type: ignore
    stretch: BoolProperty(name="Allow Stretch", default=False) # type: ignore
    pole_target: EnumProperty(
        name="Pole Target",
        description="Bone to use as Pole Target",
        items=get_pole_target_items,
        default=0,
    ) # type: ignore
    pole_angle: FloatProperty(name="Pole Angle", default=0.0) # type: ignore
    use_location: BoolProperty(name="Use Location", default=True) # type: ignore
    weight_position: FloatProperty(name="Weight Position", default=1.0, min=0.0, max=1.0) # type: ignore
    use_rotation: BoolProperty(name="Use Rotation", default=False) # type: ignore
    weight_rotation: FloatProperty(name="Weight Rotation", default=0.0, min=0.0, max=1.0) # type: ignore
    influence: FloatProperty(name="Influence", default=1.0, min=0.0, max=1.0) # type: ignore

    def invoke(self, context, event):
        if len(context.selected_pose_bones) != 2:
            self.report({'ERROR'}, "Select exactly two bones: IK target and chain root")
            return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        armature = context.active_object
        pose_bones = armature.pose.bones
        selected = context.selected_pose_bones

        selected = [b for b in selected if b.name != context.active_pose_bone.name]

        target_bone = selected[0]
        root_bone = context.active_pose_bone

        ik_constraint = root_bone.constraints.new('IK')
        ik_constraint.target = armature
        ik_constraint.subtarget = target_bone.name
        ik_constraint.chain_count = self.chain_length
        ik_constraint.iterations = self.iterations
        ik_constraint.use_tail = self.use_tail
        ik_constraint.use_stretch = self.stretch
        ik_constraint.use_location = self.use_location
        ik_constraint.use_rotation = self.use_rotation
        ik_constraint.weight = self.weight_position
        ik_constraint.orient_weight = self.weight_rotation
        ik_constraint.influence = self.influence

        if self.pole_target != 'NONE':
            ik_constraint.pole_target = armature
            ik_constraint.pole_subtarget = self.pole_target
            ik_constraint.pole_angle = self.pole_angle

        self.report({'INFO'}, f"IK constraint added to {root_bone.name}")
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(MESH_OT_johnnygizmo_ik_plus.bl_idname)


def register():
    bpy.utils.register_class(MESH_OT_johnnygizmo_ik_plus)
    bpy.types.VIEW3D_MT_pose.append(menu_func)
    bpy.types.VIEW3D_MT_pose_ik.append(menu_func)


def unregister():
    bpy.utils.unregister_class(MESH_OT_johnnygizmo_ik_plus)
    bpy.types.VIEW3D_MT_pose_ik.remove(menu_func)
    bpy.types.VIEW3D_MT_pose.remove(menu_func)
