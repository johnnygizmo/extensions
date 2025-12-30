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
from mathutils import Vector, Matrix
from math import atan2


class ARMATURE_OT_align_bone_to_face(bpy.types.Operator):
    bl_idname = "armature.align_bone_to_face"
    bl_label = "Align Active Bone to Face Normal"
    bl_description = (
        "Align the active bone's direction with a selected mesh face normal. "
        "Requires one armature and one mesh object selected, with the mesh in edit mode. "
        "If multiple bones are selected, all will move relative to the active bone's movement."
    )
    bl_options = {"REGISTER", "UNDO"}

    flip_direction: bpy.props.BoolProperty(
        name="Flip Direction",
        description="Point the bone in the opposite direction of the face normal",
        default=False,
    )

    move_to_face: bpy.props.BoolProperty(
        name="Move to Face Location",
        description="Move the bone head to the face centroid",
        default=True,
    )

    align_to_edge: bpy.props.BoolProperty(
        name="Align to Active Edge",
        description="Align bone axis perpendicular to the active edge (requires face and edge select mode)",
        default=False,
    )

    edge_axis: bpy.props.EnumProperty(
        name="Edge Align Axis",
        description="Which bone axis to align perpendicular to the edge",
        items=[
            ('X', "X Axis", "Align bone X axis perpendicular to edge"),
            ('Z', "Z Axis", "Align bone Z axis perpendicular to edge"),
        ],
        default='X',
    )

    flip_bone_roll: bpy.props.BoolProperty(
        name="Flip Roll 180°",
        description="Add 180 degrees to the bone roll (only when Align to Active Edge is enabled)",
        default=False,
    )

    move_selected_bones: bpy.props.BoolProperty(
        name="Move Selected Bones",
        description="Move all selected bones relative to the active bone's movement",
        default=True,
    )



    def read_selected_face_world(self, obj):
        """Return (centroid_world, normal_world) of the selected faces on obj or None."""
        ctx = bpy.context
        prev_active = ctx.view_layer.objects.active
        prev_mode = ctx.mode
        
        # Switch to object mode first to reliably change active
        if ctx.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        ctx.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj.data)
        faces = [f for f in bm.faces if f.select]
        
        if not faces:
            bpy.ops.object.mode_set(mode='OBJECT')
            ctx.view_layer.objects.active = prev_active
            return None

        total_area = 0.0
        centroid = Vector((0.0, 0.0, 0.0))
        normal = Vector((0.0, 0.0, 0.0))
        
        for f in faces:
            area = f.calc_area()
            # Face centroid in object space
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

        # Convert to world space
        world_centroid = obj.matrix_world @ centroid
        world_normal = (obj.matrix_world.to_3x3() @ normal).normalized()

        # Return to object mode and restore previous active
        bpy.ops.object.mode_set(mode='OBJECT')
        ctx.view_layer.objects.active = prev_active
        
        return world_centroid, world_normal

    def read_active_edge_world(self, obj):
        """Return world-space direction vector of the active edge or None."""
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

    @classmethod
    def poll(cls, context):
        # 1. Check object types and counts
        sel = context.selected_objects
        armatures = [o for o in sel if o.type == 'ARMATURE']
        meshes = [o for o in sel if o.type == 'MESH']
        
        if len(armatures) != 1 or len(meshes) != 1:
            return False
        
        arm_obj = armatures[0]
        mesh_obj = meshes[0]
        
        # 2. Check Modes
        if arm_obj.mode != 'EDIT':
            return False
        if mesh_obj.mode != 'OBJECT':
            return False
            
        # 3. Check Bone Selection (Edit Mode)
        # We need at least one selected bone and an active bone
        # Accessing edit_bones is safe because we verified mode is EDIT
        has_selected = False
        for b in arm_obj.data.edit_bones:
            if b.select:
                has_selected = True
                break
        
        if not has_selected:
            return False
        
        # Check for active bone
        if not arm_obj.data.edit_bones.active:
            return False
            
        # 4. Check Face Selection (Object Mode)
        # We need at least one selected face
        # Accessing polygons.select is safe in Object Mode
        # usage of any() ensures we stop at the first selected face, avoiding full iteration
        if not any(p.select for p in mesh_obj.data.polygons):
            return False
            
        return True

    def execute(self, context):
        # Validate selection: need exactly one armature and one mesh
        sel = context.selected_objects
        armatures = [o for o in sel if o.type == 'ARMATURE']
        meshes = [o for o in sel if o.type == 'MESH']
        
        if len(armatures) != 1 or len(meshes) != 1:
            self.report({'ERROR'}, "Select exactly one armature and one mesh object.")
            return {'CANCELLED'}
        
        armature_obj = armatures[0]
        mesh_obj = meshes[0]
        
        # Get the selected face from the mesh
        face_data = self.read_selected_face_world(mesh_obj)
        if face_data is None:
            self.report({'ERROR'}, f"No selected face found on mesh '{mesh_obj.name}'.")
            return {'CANCELLED'}
        
        face_centroid, face_normal = face_data
        
        # Apply flip if requested
        if self.flip_direction:
            face_normal = -face_normal
        
        # Switch to edit mode on armature to access bones
        prev_active = context.view_layer.objects.active
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        context.view_layer.objects.active = armature_obj
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Get the active bone
        edit_bones = armature_obj.data.edit_bones
        if not edit_bones.active:
            bpy.ops.object.mode_set(mode='OBJECT')
            context.view_layer.objects.active = prev_active
            self.report({'ERROR'}, f"No active bone in armature '{armature_obj.name}'.")
            return {'CANCELLED'}
        
        active_bone = edit_bones.active
        
        # Store initial state of all selected bones (if move_selected_bones is enabled)
        bone_offsets = {}
        if self.move_selected_bones:
            # Store the initial head and tail positions of the active bone
            active_head_initial = active_bone.head.copy()
            active_tail_initial = active_bone.tail.copy()
            active_vector_initial = active_tail_initial - active_head_initial
            active_x_axis_initial = active_bone.x_axis.copy()  # Store active bone's initial X-axis
            
            # Store offsets for all selected bones (except the active one)
            for bone in edit_bones:
                if bone.select and bone != active_bone:
                    # Store position offsets
                    bone_offsets[bone.name] = {
                        'head_offset': bone.head - active_head_initial,
                        'tail_offset': bone.tail - active_head_initial,
                        'z_axis': bone.z_axis.copy(),  # Store the bone's Z-axis (roll orientation)
                        'vector': (bone.tail - bone.head).copy(),  # Store the bone's direction vector
                    }
        
        # Always preserve the bone length
        desired_length = (active_bone.tail - active_bone.head).length
        
        # Determine bone head position (in world space)
        armature_matrix_inv = armature_obj.matrix_world.inverted()
        
        if self.move_to_face:
            # Move bone head to face centroid
            head_world = face_centroid
        else:
            # Keep the bone head position
            head_world = armature_obj.matrix_world @ active_bone.head
        
        # Calculate new tail position
        tail_world = head_world + face_normal * desired_length
        
        # Convert to armature local space
        head_local = armature_matrix_inv @ head_world
        tail_local = armature_matrix_inv @ tail_world
        
        # Set head and tail first
        active_bone.head = head_local
        active_bone.tail = tail_local
        
        print(f"DEBUG: Bone head/tail set. align_to_edge={self.align_to_edge}")
                
        # Calculate and set roll if edge alignment is enabled
        if self.align_to_edge:
            print("DEBUG: Attempting edge alignment...")
            edge_vector = self.read_active_edge_world(mesh_obj)
            print(f"DEBUG: Edge vector: {edge_vector}")
            
            if edge_vector is not None:
                # Normalize the edge vector
                edge_vector.normalize()
                
                # Get the current bone vector (already aligned to face normal)
                bone_vector = face_normal.normalized()
                
                # Project edge vector onto plane perpendicular to bone vector
                edge_projected = edge_vector - bone_vector * edge_vector.dot(bone_vector)
                print(f"DEBUG: Edge projected length: {edge_projected.length}")
                
                if edge_projected.length >= 1e-6:
                    edge_projected.normalize()
                    
                    # Calculate the target X axis for the bone in world space
                    if self.edge_axis == 'X':
                        # X axis should point along the edge direction (negated to point toward)
                        target_x_world = -edge_projected
                        print(f"DEBUG: X axis mode - target_x_world: {target_x_world}")
                    else:  # Z axis should point along the edge
                        # Z should point along edge, so X is perpendicular (negated)
                        target_x_world = -(bone_vector.cross(edge_projected).normalized())
                        print(f"DEBUG: Z axis mode - target_x_world: {target_x_world}")
                    
                    # Use Blender's built-in align_roll method with the target vector
                    # Convert to armature local space
                    target_x_local = armature_matrix_inv.to_3x3() @ target_x_world
                    print(f"DEBUG: target_x_local: {target_x_local}")
                    
                    # Re-establish armature context after reading edge (which switched to mesh)
                    # This is critical - reading the edge switched active object to mesh
                    if context.mode != 'OBJECT':
                        bpy.ops.object.mode_set(mode='OBJECT')
                    context.view_layer.objects.active = armature_obj
                    bpy.ops.object.mode_set(mode='EDIT')
                    
                    # Re-fetch the bone to ensure we have a valid reference
                    active_bone = armature_obj.data.edit_bones.active
                    print(f"DEBUG: Re-fetched active bone: {active_bone}")
                    
                    if active_bone:
                        print("DEBUG: Calling align_roll...")
                        # align_roll is the safe way - it doesn't trigger the problematic update
                        active_bone.align_roll(target_x_local)
                        
                        # Add 180 degrees if flip is requested
                        if self.flip_bone_roll:
                            import math
                            active_bone.roll += math.pi
                            print(f"DEBUG: Added 180° flip, roll = {active_bone.roll}")
                        else:
                            print(f"DEBUG: Roll aligned successfully, roll = {active_bone.roll}")
                    else:
                        print("DEBUG: Active bone lost, cannot set roll")
                else:
                    print("DEBUG: Edge projected length too small, skipping")
            else:
                print("DEBUG: No edge vector found")
        
        # Apply the transformation to all other selected bones
        if self.move_selected_bones and bone_offsets:
            # Calculate the transformation that was applied to the active bone
            active_head_final = active_bone.head.copy()
            active_tail_final = active_bone.tail.copy()
            active_vector_final = active_tail_final - active_head_final
            active_x_axis_final = active_bone.x_axis.copy()  # Get active bone's final X-axis
            
            from mathutils import Matrix
            
            # Build the initial and final orientation matrices for the active bone
            # These matrices represent the bone's full 3D orientation (direction + roll)
            
            # Initial orientation matrix
            active_y_initial = active_vector_initial.normalized()
            active_x_initial = active_x_axis_initial.normalized()
            # Z-axis is perpendicular to both X and Y
            active_z_initial = active_x_initial.cross(active_y_initial).normalized()
            
            initial_orientation = Matrix((
                active_x_initial,
                active_y_initial,
                active_z_initial
            )).transposed()
            
            # Final orientation matrix
            active_y_final = active_vector_final.normalized()
            active_x_final = active_x_axis_final.normalized()
            # Z-axis is perpendicular to both X and Y
            active_z_final = active_x_final.cross(active_y_final).normalized()
            
            final_orientation = Matrix((
                active_x_final,
                active_y_final,
                active_z_final
            )).transposed()
            
            # Calculate the rotation matrix that transforms from initial to final orientation
            # This includes BOTH the directional rotation AND the roll rotation
            rotation_matrix_3x3 = final_orientation @ initial_orientation.inverted()
            rotation_matrix = rotation_matrix_3x3.to_4x4()
            
            # Calculate translation
            translation = active_head_final - active_head_initial
            
            # Apply transformation to all other selected bones
            for bone_name, offsets in bone_offsets.items():
                bone = edit_bones.get(bone_name)
                if bone:
                    # Apply rotation to the offsets
                    head_offset_rotated = rotation_matrix @ offsets['head_offset']
                    tail_offset_rotated = rotation_matrix @ offsets['tail_offset']
                    
                    # Apply translation and set new positions FIRST
                    bone.head = active_head_final + head_offset_rotated
                    bone.tail = active_head_final + tail_offset_rotated
                    
                    # Calculate the bone's new direction
                    bone_vector_new = (bone.tail - bone.head).normalized()
                    
                    # Rotate the bone's original Z-axis by the transformation
                    rotated_z_axis = rotation_matrix_3x3 @ offsets['z_axis']
                    
                    # Project the rotated Z-axis onto the plane perpendicular to the new bone direction
                    # This ensures the Z-axis is orthogonal to the bone's Y-axis (direction)
                    z_projected = rotated_z_axis - bone_vector_new * rotated_z_axis.dot(bone_vector_new)
                    
                    if z_projected.length > 1e-6:
                        z_projected.normalize()
                        
                        print(f"DEBUG: Bone {bone_name} - Rotated Z-axis: {rotated_z_axis}")
                        print(f"DEBUG: Bone {bone_name} - Projected Z-axis: {z_projected}")
                        print(f"DEBUG: Bone {bone_name} - Roll before: {bone.roll}")
                        
                        # Use align_roll to set the bone's roll based on the projected Z-axis
                        bone.align_roll(z_projected)
                        
                        print(f"DEBUG: Bone {bone_name} - Roll after: {bone.roll}")

        # Restore Edit Mode on the Armature to preserve Redo panel context
        if context.mode != 'OBJECT':
             bpy.ops.object.mode_set(mode='OBJECT')
        
        context.view_layer.objects.active = armature_obj
        bpy.ops.object.mode_set(mode='EDIT')
        
        return {'FINISHED'}


classes = (ARMATURE_OT_align_bone_to_face,)


def register():
    for c in classes:
        bpy.utils.register_class(c)
    try:
        bpy.types.VIEW3D_MT_edit_armature.append(menu_func)
    except Exception:
        # If the menu isn't available, ignore silently
        pass


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
    try:
        bpy.types.VIEW3D_MT_edit_armature.remove(menu_func)
    except Exception:
        pass


def menu_func(self, context):
    self.layout.operator(ARMATURE_OT_align_bone_to_face.bl_idname, text="Align Bone to Face Normal")
