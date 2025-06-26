import bpy
from . import bone_picker
from . import mesh_bone_magnet
from . import armature_bone_magnet
from . import bone_straightener
from . import panel


class VIEW3D_PT_johnnygizmo_rigging_tools(bpy.types.Panel):
    bl_label = "JohnnyGizmo Rigging Tools"
    bl_idname = "VIEW3D_PT_johnnygizmo_rigging_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rigging'

    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        layout.label(text="Mesh Rigging Tools")
        if ob and ob.type == 'MESH' and ob.mode == 'EDIT' and ob.parent and ob.parent.type == 'ARMATURE':
            layout.operator("object.johnnygizmo_mesh_bone_magnet", text="Mesh Bone Magnet", icon='SNAP_ON')
            layout.operator("mesh.johnnygizmo_vertex_bone_picker", text="Vertex Bone Assignment", icon='BONE_DATA')
            layout.operator("mesh.johnnygizmo_add_bone_at_selected", text="Add Bone at Selected", icon='ADD')

        if ob and ob.type == 'ARMATURE' and ob.mode == 'EDIT':
            layout.operator("armature.johnnygizmo_armature_bone_magnet", text="Armature Bone Magnet", icon='SNAP_ON')
            layout.operator("armature.johnnygizmo_bone_straightener", text="Bone Straightener", icon='CURVE_PATH')
            layout.operator("armature.calculate_roll", text="Recalc Roll", icon='BONE_DATA')
        if ob and ob.type == 'ARMATURE' and ob.mode == 'POSE':            
            layout.operator("armature.johnnygizmo_add_ik_plus", text="Add IK Chain with Settings", icon='CON_KINEMATIC')

        arm_ob = None
        arm_disp = "Active Armature"
        if ob and ob.type == 'ARMATURE':
            arm_ob = ob
        elif ob and ob.parent and ob.parent.type == 'ARMATURE':
            arm_disp = "Parent Armature"
            arm_ob = ob.parent
    
        if arm_ob:
            box = layout.box()
            box.label(text=arm_disp+": " + arm_ob.name)
            box.row().prop(arm_ob.data, "pose_position", expand=True)
            box.prop(arm_ob.data, "display_type", text="")
            box.prop(arm_ob.data, "show_axes", text="Show Axes")
            box.prop(arm_ob.data, "axes_position", text="Axes Position")
            box.prop(arm_ob.data, "show_names", text="Show Bone Names")
            box.prop(arm_ob.data, "show_bone_custom_shapes", text="Show Custom Shapes")
           
# -*- coding: utf-8 -*-
def register():
    bpy.utils.register_class(VIEW3D_PT_johnnygizmo_rigging_tools)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_johnnygizmo_rigging_tools)