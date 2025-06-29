import bpy

from bpy.types import Operator
from bpy.props import (
    EnumProperty,
    IntProperty,
    FloatProperty,
    BoolProperty,
    StringProperty,
    PointerProperty
)

class MESH_OT_johnnygizmo_damptrackto_plus(Operator):
    bl_idname = "armature.johnnygizmo_add_damp_track_to_plus"
    bl_label = "Add Damped Track with Settings"
    bl_description = "Adds a Damped Track constraint to the selected bones"
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

   # type: ignore

    
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
       

        layout.prop(self, "influence")

    def execute(self, context):
        armature = context.active_object       
        selected = context.selected_pose_bones
        props = context.scene.johnnygizmo_rigging_tools_properties

        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Active object is not an armature.")
            return {'CANCELLED'}

        if not selected:
            self.report({'ERROR'}, "No pose bones selected.")
            return {'CANCELLED'}

        root_bone = context.active_pose_bone

        constraint = root_bone.constraints.new('DAMPED_TRACK')
        constraint.target = props.selected_object
        if props.selected_object and props.selected_object.type == 'ARMATURE' and props.selected_bone:
            constraint.subtarget = props.selected_bone
        constraint.influence = self.influence
        constraint.track_axis = self.track_axis
       
        props.selected_object = None
        props.selected_bone = ""
        props.selected_object_2 = None
        props.selected_bone_2 = ""
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(MESH_OT_johnnygizmo_damptrackto_plus.bl_idname)


def register():
    bpy.utils.register_class(MESH_OT_johnnygizmo_damptrackto_plus)
    bpy.types.VIEW3D_MT_pose.append(menu_func)
    bpy.types.VIEW3D_MT_pose_ik.append(menu_func)


def unregister():
    bpy.utils.unregister_class(MESH_OT_johnnygizmo_damptrackto_plus)
    bpy.types.VIEW3D_MT_pose_ik.remove(menu_func)
    bpy.types.VIEW3D_MT_pose.remove(menu_func)