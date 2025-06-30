import bpy # type: ignore

from bpy.types import Operator # type: ignore
from bpy.props import ( # type: ignore
    EnumProperty,
    FloatProperty,
    BoolProperty,
)

class ARMATURE_OT_johnnygizmo_stretchto_plus(Operator):
    bl_idname = "armature.johnnygizmo_add_stretch_to_plus"
    bl_label = "Add Stretch To with Settings"
    bl_description = "Adds a Stretch To constraint to the selected bones"
    bl_options = {'REGISTER', 'UNDO'}

    rest_length: FloatProperty(
        name="Original Length",
        description="Original length of the bone before stretching",
        default=0.0,
        min=0.0
    )  # type: ignore
    bulge: FloatProperty(
        name="Volume Variation",
        description="Amount of volume variation during stretching",
        default=1.0,
        min=0.0
    )  # type: ignore
    use_bulge_min: BoolProperty(
        name="Use Bulge Min",
        description="Enable minimum bulge value",
        default=False
    )  # type: ignore
    use_bulge_max: BoolProperty(
        name="Use Bulge Max",
        description="Enable maximum bulge value",
        default=False
    )  # type: ignore
    bulge_min: FloatProperty(
        name="Bulge Min",
        description="Minimum bulge value",
        default=1.0,
        min=0.0
    )  # type: ignore
    bulge_max: FloatProperty(
        name="Bulge Max",
        description="Maximum bulge value",
        default=1.0,
        min=0.0
    )  # type: ignore

    bulge_smooth: FloatProperty(
        name="Bulge Smooth",
        description="Smoothness of the bulge effect",
        default=0.0,
        min=0.0,
        max=1.0
    )  # type: ignore

    volume: EnumProperty(
        name="Volume",
        description="Maintain the object volume during stretching",
        items=[
            ('VOLUME_XZX', "XZ", "Calculate volume based on XZ plane"),
            ('VOLUME_X', "X", "Calculate volume based on X axis"),
            ('VOLUME_Z', "Z", "Calculate volume based on Z axis"),
            ("NO_VOLUME", "None", "Do not maintain volume"),

        ],
        default='VOLUME_XZX'
    )  # type: ignore

    keep_axis: EnumProperty(
        name="Rotation",
        description="Rotation type and axis to keep aligned",
        items=[
            ('PLANE_X', "XZ", "Rotate around local X then Z axis"),
            ('PLANE_Z', "ZX", "Rotate around local Z then X axis"),
            ('SWING_Y', "Swing", "Use smallest single rotation"),
        ],
        default='SWING_Y'
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
        layout.label(text="Stetch Target Object:")
        layout = self.layout
        layout.prop_search(props, "selected_object", context.scene, "objects", text="")
        
        if props.selected_object and props.selected_object.type == 'ARMATURE':
            layout.prop_search(
                props,
                "selected_bone",
                props.selected_object.data,
                "bones",
                text="Target Bone"
            )
        
        #layout.prop(self, "rest_length")
        layout.prop(self, "bulge")
        row = layout.row()
        row.prop(self, "use_bulge_min")
        row.prop(self, "bulge_min")
        row = layout.row()
        row.prop(self, "use_bulge_max")
        row.prop(self, "bulge_max")
        layout.prop(self, "bulge_smooth")
        row = layout.row()
        row.label(text="Volume:")
        row.prop_enum(self, "volume", 'VOLUME_XZX', text="XZ")
        row.prop_enum(self, "volume", 'VOLUME_X', text="X")
        row.prop_enum(self, "volume", 'VOLUME_Z', text="Z")
        row.prop_enum(self, "volume", 'NO_VOLUME', text="None")
        
        row = layout.row()
        row.label(text="Keep Axis:")
        row.prop_enum(self, "keep_axis", 'PLANE_X', text="XZ")
        row.prop_enum(self, "keep_axis", 'PLANE_Z', text="ZX")
        row.prop_enum(self, "keep_axis", 'SWING_Y', text="Swing")
        
        
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
       
        constraint = root_bone.constraints.new('STRETCH_TO')
        constraint.target = props.selected_object
        if props.selected_object and props.selected_object.type == 'ARMATURE' and props.selected_bone:
            constraint.subtarget = props.selected_bone
        constraint.influence = self.influence
        

       # constraint.rest_length = self.rest_length
        constraint.bulge = self.bulge
        constraint.use_bulge_min = self.use_bulge_min 
        constraint.use_bulge_max = self.use_bulge_max
        constraint.bulge_min = self.bulge_min
        constraint.bulge_max = self.bulge_max
        constraint.bulge_smooth = self.bulge_smooth
        constraint.volume = self.volume
        constraint.keep_axis = self.keep_axis

        props.clear()
        return {'FINISHED'}

    def cancel(self, context):
        props = context.scene.johnnygizmo_rigging_tools_properties
        props.clear()
        return {'CANCELLED'}
    
def menu_func(self, context):
    self.layout.operator(ARMATURE_OT_johnnygizmo_stretchto_plus.bl_idname)

def register():
    bpy.utils.register_class(ARMATURE_OT_johnnygizmo_stretchto_plus)
    bpy.types.VIEW3D_MT_pose.append(menu_func)
    bpy.types.VIEW3D_MT_pose_ik.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ARMATURE_OT_johnnygizmo_stretchto_plus)
    bpy.types.VIEW3D_MT_pose_ik.remove(menu_func)
    bpy.types.VIEW3D_MT_pose.remove(menu_func)