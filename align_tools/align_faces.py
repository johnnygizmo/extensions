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
from mathutils import Vector, Matrix, Quaternion    
from math import radians, atan2


class OBJECT_OT_align_face_to_face(bpy.types.Operator):
    bl_idname = "object.align_face_to_face"
    bl_label = "Align Active Face to Second Object Face"
    bl_description = (
        "Move and rotate the active object so its selected face aligns to the other "
        "selected object's selected face (normals become opposite)."
    )
    bl_options = {"REGISTER", "UNDO"}

    twist_angle: bpy.props.FloatProperty(
        name="Twist Angle",
        description="Rotation around the face normal (degrees)",
        default=0.0,
    )

    offset_distance: bpy.props.FloatProperty(
        name="Offset Distance",
        description="Translate along the target normal after alignment",
        default=0.0,
    )

    move_active: bpy.props.BoolProperty(
        name="Move Active",
        description="When checked, move the active object; otherwise move the other selected object",
        default=True,
    )

    match_normal: bpy.props.BoolProperty(
        name="Flip Normal Direction",
        description="If checked, align normals to point in the same direction; otherwise make them opposite",
        default=False,
    )

    match_edge_rotation: bpy.props.BoolProperty(
        name="Match Edge Rotation",
        description=(
            "If enabled, use the active edges from both meshes to align edge directions."
        ),
        default=False,
    )

    flip_edge_direction: bpy.props.BoolProperty(
        name="Flip Edge Direction",
        description="Add 180 degrees to the edge rotation (only when Match Edge Rotation is enabled)",
        default=False,
    )

    def read_selected_face_world(self, obj):
        """Return (centroid_world, normal_world) of the selected faces on obj or None."""
        # Ensure object is active and in edit mode to read selection
        ctx = bpy.context
        prev_active = ctx.view_layer.objects.active
        # switch to object mode first to reliably change active
        if ctx.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        ctx.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj.data)
        faces = [f for f in bm.faces if f.select]
        if not faces:
            # leave edit mode so caller can handle mode restore
            bpy.ops.object.mode_set(mode='OBJECT')
            ctx.view_layer.objects.active = prev_active
            return None

        total_area = 0.0
        centroid = Vector((0.0, 0.0, 0.0))
        normal = Vector((0.0, 0.0, 0.0))
        for f in faces:
            area = f.calc_area()
            # face centroid in object space
            verts = [v.co for v in f.verts]
            c = Vector((0.0, 0.0, 0.0))
            for v in verts:
                c += v
            c /= len(verts)
            centroid += c * area
            normal += f.normal.copy() * area
            total_area += area

        if total_area == 0.0:
            bpy.ops.object.mode_set(mode='OBJECT')
            ctx.view_layer.objects.active = prev_active
            return None

        centroid /= total_area
        normal = normal.normalized()

        # convert to world space
        world_centroid = obj.matrix_world @ centroid
        world_normal = (obj.matrix_world.to_3x3() @ normal).normalized()

        # return to object mode and restore previous active
        bpy.ops.object.mode_set(mode='OBJECT')
        ctx.view_layer.objects.active = prev_active
        return world_centroid, world_normal

    def execute(self, context):
        sel = [o for o in context.selected_objects if o.type == 'MESH']
        if len(sel) != 2 or context.active_object is None:
            self.report({'ERROR'}, "Select exactly two mesh objects (one active).")
            return {'CANCELLED'}

        active = context.active_object
        others = [o for o in sel if o != active]
        if not others:
            self.report({'ERROR'}, "Couldn't determine the inactive mesh.")
            return {'CANCELLED'}
        other = others[0]

        active_face = self.read_selected_face_world(active)
        if active_face is None:
            self.report({'ERROR'}, f"No selected face found on active object '{active.name}'.")
            return {'CANCELLED'}

        other_face = self.read_selected_face_world(other)
        if other_face is None:
            self.report({'ERROR'}, f"No selected face found on other object '{other.name}'.")
            return {'CANCELLED'}

        active_pos, active_norm = active_face
        other_pos, other_norm = other_face

        # Compute rotation quaternion to make active_norm point opposite to other_norm
        # Branch: either move the active object (default) or move the other object
        if self.move_active:
            mover = active
            mover_pos = active_pos
            mover_norm = active_norm
            fixed_pos = other_pos
            fixed_norm = other_norm
            delta = fixed_pos - mover_pos
        else:
            mover = other
            mover_pos = other_pos
            mover_norm = other_norm
            fixed_pos = active_pos
            fixed_norm = active_norm
            delta = fixed_pos - mover_pos

        # Decide whether normals should match direction or be opposite
        target = fixed_norm if self.match_normal else -fixed_norm

        try:
            q_align = mover_norm.rotation_difference(target)
        except Exception:
            self.report({'ERROR'}, "Failed to compute rotation difference between normals.")
            return {'CANCELLED'}

        R_align = q_align.to_matrix().to_4x4()

        # Helper: read active edge on an object and return its world-space direction
        def read_active_edge_world(obj):
            ctx = bpy.context
            prev_active = ctx.view_layer.objects.active
            if ctx.mode != 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
            ctx.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bm = bmesh.from_edit_mesh(obj.data)
            
            # Get the active edge from selection history
            active_elem = bm.select_history.active
            if active_elem is None or not isinstance(active_elem, bmesh.types.BMEdge):
                bpy.ops.object.mode_set(mode='OBJECT')
                ctx.view_layer.objects.active = prev_active
                return None
            
            # Calculate world-space direction vector
            mw3 = obj.matrix_world.to_3x3()
            v1 = active_elem.verts[0].co
            v2 = active_elem.verts[1].co
            vec = (v2 - v1)
            vec_world = mw3 @ vec
            
            bpy.ops.object.mode_set(mode='OBJECT')
            ctx.view_layer.objects.active = prev_active
            return vec_world

        # Determine twist angle either from active edges or from the twist_angle property
        twist_rad = 0.0
        if self.match_edge_rotation:

            edge_active_world = read_active_edge_world(active)
            edge_other_world = read_active_edge_world(other)
            
            if edge_active_world is None:
                self.report({'ERROR'}, f"No active edge found on active object '{active.name}'.")
                return {'CANCELLED'}
            if edge_other_world is None:
                self.report({'ERROR'}, f"No active edge found on other object '{other.name}'.")
                return {'CANCELLED'}

            if self.move_active:
                mover_edge = edge_active_world
                fixed_edge = edge_other_world
            else:
                mover_edge = edge_other_world
                fixed_edge = edge_active_world

            # Apply the alignment rotation to the mover edge to compare post-align directions
            mover_edge_rot = R_align.to_3x3() @ mover_edge

            axis = target.normalized()

            def project_plane(v, n):
                return (v - n * v.dot(n))

            a = project_plane(mover_edge_rot, axis)
            b = project_plane(fixed_edge, axis)
            if a.length < 1e-6 or b.length < 1e-6:
                self.report({'ERROR'}, "Selected edge direction too small to compute rotation.")
                return {'CANCELLED'}
            a.normalize()
            b.normalize()

            cross = a.cross(b)
            dot = max(-1.0, min(1.0, a.dot(b)))
            signed = atan2(axis.dot(cross), dot)
            twist_rad = signed
            
            # Add π if flip_edge_direction is enabled
            if self.flip_edge_direction:
                twist_rad += 3.141592653589793  # π
        else:
            twist_rad = radians(self.twist_angle) if abs(self.twist_angle) > 1e-6 else 0.0

        # Build total rotation: align rotation plus twist about target normal
        R_total = R_align
        if abs(twist_rad) > 1e-12:
            R_twist = Quaternion(target.normalized(), twist_rad).to_matrix().to_4x4()
            R_total = R_twist @ R_align

        # Ensure we are in object mode before modifying matrix_world
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        M = mover.matrix_world.copy()

        # Rotate around the face centroid so that centroid stays in place after rotation
        M_rot = Matrix.Translation(mover_pos) @ R_total @ Matrix.Translation(-mover_pos) @ M

        # After rotation, translate so centroids coincide
        M_translated = Matrix.Translation(delta) @ M_rot

        # Apply offset along the target normal (positive moves along target)
        if abs(self.offset_distance) > 1e-6:
            M_final = Matrix.Translation(self.offset_distance * target) @ M_translated
        else:
            M_final = M_translated

        mover.matrix_world = M_final

        return {'FINISHED'}


classes = (OBJECT_OT_align_face_to_face,)


def register():
    for c in classes:
        bpy.utils.register_class(c)
    try:
        bpy.types.VIEW3D_MT_edit_mesh_transform.append(menu_func)
    except Exception:
        # If the menu isn't available (older/newer Blender), ignore silently
        pass


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
    try:
        bpy.types.VIEW3D_MT_edit_mesh_transform.remove(menu_func)
    except Exception:
        pass


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_align_face_to_face.bl_idname, text="Align Face To Face")

