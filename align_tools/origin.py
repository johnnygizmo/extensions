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
from mathutils import Vector


class OBJECT_OT_origin_to_bbox(bpy.types.Operator):
    bl_idname = "object.origin_to_bbox"
    bl_label = "Set Origin to Bounding Box Position"
    bl_description = (
        "Set origin to center of geometry, then move it to a specified position "
        "based on the object's bounding box (Top/Center/Bottom, Left/Center/Right, Front/Center/Back)"
    )
    bl_options = {"REGISTER", "UNDO"}

    # Vertical position
    vertical: bpy.props.EnumProperty(
        name="Vertical",
        description="Vertical position on the bounding box",
        items=[
            ('TOP', "Top", "Top of bounding box"),
            ('CENTER', "Center", "Center of bounding box (vertical)"),
            ('BOTTOM', "Bottom", "Bottom of bounding box"),
        ],
        default='BOTTOM',
    )

    # Horizontal position (Left-Right)
    horizontal: bpy.props.EnumProperty(
        name="Horizontal",
        description="Horizontal position on the bounding box (Left-Right axis)",
        items=[
            ('LEFT', "Left", "Left side of bounding box"),
            ('CENTER', "Center", "Center of bounding box (horizontal)"),
            ('RIGHT', "Right", "Right side of bounding box"),
        ],
        default='CENTER',
    )

    # Depth position (Front-Back)
    depth: bpy.props.EnumProperty(
        name="Depth",
        description="Depth position on the bounding box (Front-Back axis)",
        items=[
            ('FRONT', "Front", "Front of bounding box"),
            ('CENTER', "Center", "Center of bounding box (depth)"),
            ('BACK', "Back", "Back of bounding box"),
        ],
        default='CENTER',
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'

    def execute(self, context):
        obj = context.active_object
        
        # Store the current mode
        initial_mode = obj.mode
        
        # Switch to object mode to ensure we can manipulate the origin
        if initial_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        # First, set origin to geometry center
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        
        # If all positions are CENTER, we're done
        if self.vertical == 'CENTER' and self.horizontal == 'CENTER' and self.depth == 'CENTER':
            if initial_mode != 'OBJECT':
                bpy.ops.object.mode_set(mode=initial_mode)
            return {'FINISHED'}
        
        # Calculate the bounding box in world space
        bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
        
        # Find min and max coordinates
        min_x = min(corner.x for corner in bbox_corners)
        max_x = max(corner.x for corner in bbox_corners)
        min_y = min(corner.y for corner in bbox_corners)
        max_y = max(corner.y for corner in bbox_corners)
        min_z = min(corner.z for corner in bbox_corners)
        max_z = max(corner.z for corner in bbox_corners)
        
        # Calculate center of bounding box
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        center_z = (min_z + max_z) / 2
        
        # Determine target position based on selections
        # Horizontal (X-axis in Blender: Left = -X, Right = +X)
        if self.horizontal == 'LEFT':
            target_x = min_x
        elif self.horizontal == 'RIGHT':
            target_x = max_x
        else:  # CENTER
            target_x = center_x
        
        # Depth (Y-axis in Blender: Front = -Y, Back = +Y)
        if self.depth == 'FRONT':
            target_y = min_y
        elif self.depth == 'BACK':
            target_y = max_y
        else:  # CENTER
            target_y = center_y
        
        # Vertical (Z-axis: Bottom = -Z, Top = +Z)
        if self.vertical == 'BOTTOM':
            target_z = min_z
        elif self.vertical == 'TOP':
            target_z = max_z
        else:  # CENTER
            target_z = center_z
        
        # Current origin position in world space
        current_origin = obj.matrix_world.translation.copy()
        
        # Calculate the offset needed in world space
        target_position = Vector((target_x, target_y, target_z))
        offset_world = target_position - current_origin
        
        # Convert offset to local space
        offset_local = obj.matrix_world.inverted().to_3x3() @ offset_world
        
        # Move the mesh geometry in the opposite direction (in local space)
        mesh = obj.data
        for vertex in mesh.vertices:
            vertex.co -= offset_local
        
        # Update the mesh
        mesh.update()
        
        # Move the object's origin to the target position
        obj.matrix_world.translation = target_position
        
        # Restore the original mode
        if initial_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode=initial_mode)
        
        return {'FINISHED'}


def draw(self, context):
    self.layout.separator()
    self.layout.operator(OBJECT_OT_origin_to_bbox.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_OT_origin_to_bbox)
    bpy.types.VIEW3D_MT_object.append(draw)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw)

def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw)
    bpy.types.VIEW3D_MT_object.remove(draw)
    bpy.utils.unregister_class(OBJECT_OT_origin_to_bbox)


if __name__ == "__main__":
    register()
