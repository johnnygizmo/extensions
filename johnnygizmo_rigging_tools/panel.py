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
        layout.operator("armature.johnnygizmo_armature_bone_magnet", text="Armature Bone Magnet", icon='SNAP_ON')
        layout.operator("object.johnnygizmo_mesh_bone_magnet", text="Mesh Bone Magnet", icon='SNAP_ON')
        layout.operator("mesh.johnnygizmo_vertex_bone_picker", text="Vertex Bone Assignment", icon='BONE_DATA')
        layout.operator("armature.johnnygizmo_bone_straightener", text="Bone Straightener", icon='CURVE_PATH')

def register():
    bpy.utils.register_class(VIEW3D_PT_johnnygizmo_rigging_tools)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_johnnygizmo_rigging_tools)