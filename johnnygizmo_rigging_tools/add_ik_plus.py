import bpy # type: ignore
from bpy.types import Operator # type: ignore
from bpy.props import ( # type: ignore
    EnumProperty,
    IntProperty,
    FloatProperty,
    BoolProperty,
    StringProperty,
    PointerProperty
)


class ARMATURE_OT_johnnygizmo_ik_plus(Operator):
    bl_idname = "armature.johnnygizmo_add_ik_plus"
    bl_label = "Add IK Chain with Settings"
    bl_description = "Adds an IK constraint to the selected bones"
    bl_options = {'REGISTER', 'UNDO'}

    chain_length: IntProperty(name="Chain Length", default=2, min=0)  # type: ignore
    iterations: IntProperty(name="Iterations", default=500, min=1)  # type: ignore
    use_tail: BoolProperty(name="Use Tail", default=True)  # type: ignore
    stretch: BoolProperty(name="Allow Stretch", default=False)  # type: ignore

    pole_target_bone: StringProperty(
        name="Pole Target Bone",
        description="Bone within the Pole Target Object to use as target"
    )  # type: ignore
    pole_angle: FloatProperty(name="Pole Angle", default=0.0, unit='ROTATION')  # type: ignore
    use_location: BoolProperty(name="Use Location", default=True)  # type: ignore
    weight_position: FloatProperty(name="Weight Position", default=1.0, min=0.0, max=1.0)  # type: ignore
    use_rotation: BoolProperty(name="Use Rotation", default=False)  # type: ignore
    weight_rotation: FloatProperty(name="Weight Rotation", default=0.0, min=0.0, max=1.0)  # type: ignore
    influence: FloatProperty(name="Influence", default=1.0, min=0.0, max=1.0)  # type: ignore





            
    def invoke(self, context, event):
        props = context.scene.johnnygizmo_rigging_tools_properties
        selected_pose_bones = context.selected_pose_bones
        active_pose_bone = context.active_pose_bone

        if active_pose_bone and active_pose_bone.parent:
            self.chain_length = 1

        if len(selected_pose_bones) == 2:
            armature = context.active_object
            props.selected_object = armature

            # Find the inactive bone among the two selected
            inactive_bone = None
            for bone in selected_pose_bones:
                if bone != active_pose_bone:
                    inactive_bone = bone
                    break
            if inactive_bone:
                props.selected_bone = inactive_bone.name
        elif len(selected_pose_bones) == 1:
            props.selected_object = None
            props.selected_bone = ""
        else:
            self.report({'ERROR'}, "Select one or two pose bones to use this operator.")
            return {'CANCELLED'}

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "chain_length")
        layout.prop(self, "iterations")
        layout.prop(self, "use_tail")
        layout.prop(self, "stretch")

        props = context.scene.johnnygizmo_rigging_tools_properties
        layout.label(text="IK Target Object:")
        layout = self.layout
        layout.prop_search(props, "selected_object", context.scene, "objects", text="")
        if props.selected_object and props.selected_object.type == 'ARMATURE':
            layout.prop_search(
                props,
                "selected_bone",
                props.selected_object.data,
                "bones",
                text="IK Target Bone"
            )
        layout.label(text="Pole Target Object:")
        layout = self.layout
        layout.prop_search(props, "selected_object_2", context.scene, "objects", text="")
        if props.selected_object_2 and props.selected_object_2.type == 'ARMATURE':
            layout.prop_search(
                props,
                "selected_bone_2",
                props.selected_object_2.data,
                "bones",
                text="Pole Target Bone"
            )
            layout.prop(self, "pole_angle")

        layout.prop(self, "use_location")
        layout.prop(self, "weight_position")
        layout.prop(self, "use_rotation")
        layout.prop(self, "weight_rotation")
        layout.prop(self, "influence")

    def cancel(self, context):
        props = context.scene.johnnygizmo_rigging_tools_properties
        props.clear()
        return {'CANCELLED'}


    def execute(self, context):
        armature = context.active_object
        pose_bones = armature.pose.bones
        selected = context.selected_pose_bones
        props = context.scene.johnnygizmo_rigging_tools_properties

        if not armature or armature.type != 'ARMATURE':
            props.clear()
            self.report({'ERROR'}, "Active object is not an armature.")
            return {'CANCELLED'}

        if not selected:
            props.clear()
            self.report({'ERROR'}, "No pose bones selected.")
            return {'CANCELLED'}

        root_bone = context.active_pose_bone
       
        ik_constraint = root_bone.constraints.new('IK')
        ik_constraint.target = props.selected_object
        if props.selected_object.type == 'ARMATURE' and props.selected_bone:
            ik_constraint.subtarget = props.selected_bone
        ik_constraint.chain_count = self.chain_length
        ik_constraint.iterations = self.iterations
        ik_constraint.use_tail = self.use_tail
        ik_constraint.use_stretch = self.stretch
        ik_constraint.use_location = self.use_location
        ik_constraint.use_rotation = self.use_rotation
        ik_constraint.weight = self.weight_position
        ik_constraint.orient_weight = self.weight_rotation
        ik_constraint.influence = self.influence

        if props.selected_object_2:
            ik_constraint.pole_target = props.selected_object_2
            if props.selected_object_2.type == 'ARMATURE' and props.selected_bone_2:
                ik_constraint.pole_subtarget = props.selected_bone_2
            else:
                ik_constraint.pole_subtarget = ""
            ik_constraint.pole_angle = self.pole_angle

        props.clear()
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(ARMATURE_OT_johnnygizmo_ik_plus.bl_idname)


def register():
    bpy.utils.register_class(ARMATURE_OT_johnnygizmo_ik_plus)
    bpy.types.VIEW3D_MT_pose.append(menu_func)
    bpy.types.VIEW3D_MT_pose_ik.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ARMATURE_OT_johnnygizmo_ik_plus)
    bpy.types.VIEW3D_MT_pose_ik.remove(menu_func)
    bpy.types.VIEW3D_MT_pose.remove(menu_func)