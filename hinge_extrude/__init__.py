# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
import bmesh
from bpy.types import Operator
from bpy.props import FloatProperty, IntProperty

bl_info = {
    "name": "Hinge Extrude",
    "author": "Johnny Matthews",
    "description": "Extrude faces rotating around an active edge",
    "blender": (4, 2, 0),
    "version": (1, 0, 0),
    "location": "View3D > Edit Mode > Mesh",
    "warning": "",
    "category": "Mesh",
}


class MESH_OT_hinge_extrude(Operator):
    """Extrude selected faces rotating around the active edge"""
    bl_idname = "mesh.hinge_extrude"
    bl_label = "Hinge Extrude"
    bl_options = {'REGISTER', 'UNDO'}

    angle: FloatProperty(
        name="Rotation Angle",
        description="Angle to rotate the extrusion around the active edge",
        default=0.785398,  # 45 degrees in radians
        min=-6.28319,  # -360 degrees
        max=6.28319,   # 360 degrees
        subtype='ANGLE'
    )
    
    steps: IntProperty(
        name="Steps",
        description="Number of extrusion steps",
        default=1,
        min=1,
        max=100
    )

    @classmethod
    def poll(cls, context):
        obj = context.object
        if obj is None or obj.type != 'MESH' or obj.mode != 'EDIT':
            return False

        # Only available if face and edge mode are enabled
        tool_settings = context.tool_settings
        if not (tool_settings.mesh_select_mode[1] and tool_settings.mesh_select_mode[2]):
            return False

        # Check for at least one face selected and one active edge
        # Note: We use total_edge_sel as a proxy for active edge in poll for performance
        mesh = obj.data
        return mesh.total_face_sel > 0 and mesh.total_edge_sel > 0

    def execute(self, context):
        obj = context.object
        mesh = obj.data
        
        # Save current settings
        saved_pivot = context.scene.tool_settings.transform_pivot_point
        saved_orientation = context.scene.transform_orientation_slots[0].type
        saved_cursor_location = context.scene.cursor.location.copy()
        saved_select_mode = context.tool_settings.mesh_select_mode[:]
        
        # Get bmesh
        bm = bmesh.from_edit_mesh(mesh)
        
        # Check if there's an active edge
        if bm.select_history.active is None or not isinstance(bm.select_history.active, bmesh.types.BMEdge):
            self.report({'ERROR'}, "No active edge selected. Please select an edge and make it active.")
            return {'CANCELLED'}
        
        active_edge = bm.select_history.active
        
        # Get selected faces
        selected_faces = [f for f in bm.faces if f.select]
        
        if not selected_faces:
            self.report({'ERROR'}, "No faces selected.")
            return {'CANCELLED'}
        
        # Update mesh to apply bmesh changes
        bmesh.update_edit_mesh(mesh)
        
        # Step 1: Select only the edge and create orientation
        bpy.ops.mesh.select_all(action='DESELECT')
        active_edge.select = True
        bmesh.update_edit_mesh(mesh)
        
        # Step 2: Create orientation from selected edge
        bpy.ops.transform.create_orientation(use=True)
        
        # Step 3: Snap cursor to selected edge
        bpy.ops.view3d.snap_cursor_to_selected()
        
        # Step 4: Set pivot to cursor
        context.scene.tool_settings.transform_pivot_point = 'CURSOR'
        
        # Step 5: Set orientation to 'Edge'
        context.scene.transform_orientation_slots[0].type = 'Edge'
        
        # Step 6: Reselect the faces
        bpy.ops.mesh.select_all(action='DESELECT')
        for f in selected_faces:
            if f.is_valid:
                f.select = True
        bmesh.update_edit_mesh(mesh)
        
        # Perform extrusion with rotation steps
        angle_step = self.angle / self.steps
        
        # Track newly created vertices if more than one step
        use_tracking = self.steps > 1
        vg = None
        if use_tracking:
            vg = obj.vertex_groups.new(name="Hinge_Extrude_Temp")
            obj.vertex_groups.active_index = vg.index

        for i in range(self.steps):
            # Step 7: Extrude with zero translation
            bpy.ops.mesh.extrude_region_move(
                MESH_OT_extrude_region={
                    "use_normal_flip": False,
                    "use_dissolve_ortho_edges": False,
                    "mirror": False
                },
                TRANSFORM_OT_translate={
                    "value": (0, 0, 0),
                    "orient_type": 'GLOBAL',
                    "constraint_axis": (False, False, False),
                    "mirror": False,
                    "use_proportional_edit": False,
                    "snap": False,
                    "release_confirm": False,
                    "use_accurate": False
                }
            )
            
            # Step 8: Rotate on Y axis with Edge orientation
            bpy.ops.transform.rotate(
                value=angle_step,
                orient_axis='Y',
                orient_type='Edge',
                mirror=True,
                use_proportional_edit=False,
                snap=False
            )
            
            if use_tracking:
                bpy.ops.object.vertex_group_assign()
        
        if use_tracking:
            bpy.ops.object.vertex_group_select()
        
        # Step 9: Select more
        bpy.ops.mesh.select_more()
        
        # Step 10: Switch to vertex mode
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        
        # Step 11: Remove doubles
        bpy.ops.mesh.remove_doubles()
        
        # Clean up the custom orientation
        try:
            bpy.ops.transform.delete_orientation()
        except:
            pass
            
        if use_tracking and vg:
            obj.vertex_groups.remove(vg)
        
        # Restore all settings
        context.scene.tool_settings.transform_pivot_point = saved_pivot
        
        # Only restore orientation if it's a built-in type, not a custom one
        builtin_orientations = {'GLOBAL', 'LOCAL', 'NORMAL', 'GIMBAL', 'VIEW', 'CURSOR', 'PARENT'}
        if saved_orientation in builtin_orientations:
            context.scene.transform_orientation_slots[0].type = saved_orientation
        else:
            # If it was a custom orientation, set to GLOBAL as default
            context.scene.transform_orientation_slots[0].type = 'GLOBAL'
        
        context.scene.cursor.location = saved_cursor_location
        context.tool_settings.mesh_select_mode = saved_select_mode
        
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(MESH_OT_hinge_extrude.bl_idname, text="Hinge Extrude")


def register():
    bpy.utils.register_class(MESH_OT_hinge_extrude)
    bpy.types.VIEW3D_MT_edit_mesh_extrude.append(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_faces.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_faces.remove(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_extrude.remove(menu_func)
    bpy.utils.unregister_class(MESH_OT_hinge_extrude)
