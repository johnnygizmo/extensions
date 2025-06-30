import bpy # type: ignore

from bpy.types import Operator # type: ignore
from bpy.props import ( # type: ignore
    EnumProperty,
    FloatProperty,
    BoolProperty,
)

class ARMATURE_OT_johnnygizmo_trackto_plus(Operator):
    bl_idname = "armature.johnnygizmo_add_track_to_plus"
    bl_label = "Add Track To with Settings"
    bl_description = "Adds a Track To constraint to the selected bones"
    bl_options = {'REGISTER', 'UNDO'}

    track_axis: EnumProperty(
        name="Track Axis",
        description="Axis to track the target object",
        items=[
            ('TRACK_X', "X Axis", ""),
            ('TRACK_Y', "Y Axis", ""),
            ('TRACK_Z', "Z Axis", ""),
            ('TRACK_NEGATIVE_X', "-X Axis", ""),
            ('TRACK_NEGATIVE_Y', "-Y Axis", ""),
            ('TRACK_NEGATIVE_Z', "-Z Axis", "")
        ],
        default='TRACK_Y'
    )  # type: ignore

    up_axis: EnumProperty(
        name="Up Axis",
        description="Axis to use as the up direction",
        items=[
            ('UP_X', "X Axis", ""),
            ('UP_Y', "Y Axis", ""),
            ('UP_Z', "Z Axis", "")
        ],
        default='UP_Z'
    )  # type: ignore

    target_z: BoolProperty(name="Target Z", default=False)  # type: ignore
    target_space: EnumProperty(
        name="Target Space",
        description="Space in which the target object is defined",
        items=[
            ('LOCAL', "Local", ""),
            ('WORLD', "World", ""),
            ('CUSTOM', "Custom", "")
        ],
        default='WORLD'
    )  # type: ignore
    owner_space: EnumProperty(
        name="Owner Space",
        description="Space in which the owner object is defined",
        items=[            
            ('WORLD', "World", ""),
            ('CUSTOM', "Custom", ""),
            ('POSE', "Pose", ""),
            ('LOCAL_WITH_PARENT', "Local With Parent", ""),
            ('LOCAL', "Local", ""),
        ],
        default='WORLD'
    )  # type: ignore
    influence: FloatProperty(name="Influence", default=1.0, min=0.0, max=1.0)  # type: ignore
            
    def invoke(self, context, event):
        props = context.scene.johnnygizmo_rigging_tools_properties
        selected_pose_bones = context.selected_pose_bones
        active_pose_bone = context.active_pose_bone

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
            props.clear()
            return {'CANCELLED'}

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        props = context.scene.johnnygizmo_rigging_tools_properties
        layout.label(text="Track Target Object:")
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
        layout.prop(self, "track_axis")
        layout.prop(self, "up_axis")
        layout.prop(self, "target_z")

        layout.prop(self, "target_space")
        layout.prop(self, "owner_space")

        if self.target_space == 'CUSTOM' or self.owner_space == 'CUSTOM':
            layout.label(text="Owner:")
            layout = self.layout
            layout.prop_search(props, "selected_object_2", context.scene, "objects", text="")
            if props.selected_object_2 and props.selected_object_2.type == 'ARMATURE':
                layout.prop_search(
                    props,
                    "selected_bone_2",
                    props.selected_object_2.data,
                    "bones",
                    text="Custom Owner Bone"
                )                
        layout.prop(self, "influence")

    def execute(self, context):
        armature = context.active_object       
        selected = context.selected_pose_bones
        props = context.scene.johnnygizmo_rigging_tools_properties

        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Active object is not an armature.")
            props.clear()
            return {'CANCELLED'}

        if not selected:
            self.report({'ERROR'}, "No pose bones selected.")
            props.clear()
            return {'CANCELLED'}

        root_bone = context.active_pose_bone
       
        constraint = root_bone.constraints.new('TRACK_TO')
        constraint.target = props.selected_object
        if props.selected_object and props.selected_object.type == 'ARMATURE' and props.selected_bone:
            constraint.subtarget = props.selected_bone
        constraint.influence = self.influence
        
        constraint.track_axis = self.track_axis
        constraint.up_axis = self.up_axis
        constraint.target_space = self.target_space
        constraint.owner_space = self.owner_space
        constraint.use_target_z = self.target_z
        if self.target_space == 'CUSTOM' or self.owner_space == 'CUSTOM':
            constraint.space_object = props.selected_object_2
            if props.selected_object_2 and props.selected_object_2.type == 'ARMATURE':
                constraint.space_subtarget = props.selected_bone_2
            else:
                constraint.space_subtarget = ""
        else:
            constraint.space_object = None
            constraint.space_subtarget = ""

        props.clear()
        return {'FINISHED'}

    def cancel(self, context):
        props = context.scene.johnnygizmo_rigging_tools_properties
        props.clear()
        return {'CANCELLED'}

def menu_func(self, context):
    self.layout.operator(ARMATURE_OT_johnnygizmo_trackto_plus.bl_idname)


def register():
    bpy.utils.register_class(ARMATURE_OT_johnnygizmo_trackto_plus)
    bpy.types.VIEW3D_MT_pose.append(menu_func)
    bpy.types.VIEW3D_MT_pose_ik.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ARMATURE_OT_johnnygizmo_trackto_plus)
    bpy.types.VIEW3D_MT_pose_ik.remove(menu_func)
    bpy.types.VIEW3D_MT_pose.remove(menu_func)