import bpy # type: ignore
from mathutils import Vector, Matrix # type: ignore

class MESH_OT_johnnygizmo_bone_straightener(bpy.types.Operator):
    bl_idname = "armature.johnnygizmo_bone_straightener"
    bl_label = "Bone Straightener"
    bl_options = {'REGISTER', 'UNDO'}

    axis: bpy.props.EnumProperty(
        name="Axis",
        items=[
            ('X+', "+X", ""),
            ('X-', "-X", ""),
            ('Y+', "+Y", ""),
            ('Y-', "-Y", ""),
            ('Z+', "+Z", ""),
            ('Z-', "-Z", "")
        ],
        default='Y+'
    ) # type: ignore

    # space: bpy.props.EnumProperty(
    #     name="Space",
    #     items=[
    #         ('LOCAL', "Local", "Use local bone space"),
    #         ('GLOBAL', "Global", "Use world space")
    #     ],
    #     default='GLOBAL'
    # )

    length: bpy.props.FloatProperty(
        name="Length",
        description="Length of the bone after aligning (0 = keep current)",
        default=1.0,
        min=0.0
    ) # type: ignore

    def invoke(self, context, event):
        obj = context.object
        if obj.type != 'ARMATURE' or context.mode != 'EDIT_ARMATURE':
            self.report({'ERROR'}, "Must be in Edit Mode on an Armature")
            return {'CANCELLED'}    
        bones = context.selected_editable_bones
        if not bones:
            self.report({'ERROR'}, "No editable bones selected")
            return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):
        obj = context.object
        if obj.type != 'ARMATURE' or context.mode != 'EDIT_ARMATURE':
            self.report({'ERROR'}, "Must be in Edit Mode on an Armature")
            return {'CANCELLED'}

        bones = context.selected_editable_bones
        if not bones:
            self.report({'ERROR'}, "No editable bones selected")
            return {'CANCELLED'}

        # Global axis direction (world space)
        axis_direction = {
            'X+': Vector((1, 0, 0)),
            'X-': Vector((-1, 0, 0)),
            'Y+': Vector((0, 1, 0)),
            'Y-': Vector((0, -1, 0)),
            'Z+': Vector((0, 0, 1)),
            'Z-': Vector((0, 0, -1)),
        }[self.axis]

        for bone in bones:
            direction = axis_direction.copy()

            # if self.space == 'LOCAL' and bone.parent:
            #     # Transform into parent bone space
            #     parent = bone.parent
            #     parent_y = (parent.tail - parent.head).normalized()
            #     parent_x = parent_y.orthogonal()
            #     parent_z = parent_y.cross(parent_x).normalized()
            #     parent_x = parent_z.cross(parent_y).normalized()

            #     parent_matrix = Matrix((parent_x, parent_y, parent_z)).transposed()
            #     direction = parent_matrix @ direction

            #elif self.space == 'GLOBAL':
                # Convert global direction into armature (edit bone) space
            armature_matrix = obj.matrix_world.inverted().to_3x3()
            direction = armature_matrix @ direction

            direction.normalize()

            # Determine bone length
            current_length = (bone.tail - bone.head).length
            target_length = self.length if self.length > 0 else current_length

            bone.tail = bone.head + direction * target_length

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(MESH_OT_johnnygizmo_bone_straightener.bl_idname, icon='CURVE_PATH')

def register():
    bpy.utils.register_class(MESH_OT_johnnygizmo_bone_straightener)
    bpy.types.VIEW3D_MT_edit_armature.append(menu_func)

def unregister():
    bpy.utils.unregister_class(MESH_OT_johnnygizmo_bone_straightener)
    bpy.types.VIEW3D_MT_edit_armature.remove(menu_func)
