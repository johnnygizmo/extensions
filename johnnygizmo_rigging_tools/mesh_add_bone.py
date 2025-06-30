import bpy # type: ignore
import bmesh # type: ignore
from mathutils import Vector # type: ignore

class OBJECT_OT_johnnygizmo_add_bone_at_selected(bpy.types.Operator):
    bl_idname = "mesh.johnnygizmo_add_bone_at_selected"
    bl_label = "Add Bone at Selected"
    bl_description = "Add a bone to the parent armature at the center of selected vertices"
    bl_options = {'REGISTER','UNDO'}


    bone_name: bpy.props.StringProperty(
        name="Bone Name",
        description="Name for the new bone",
        default="Bone",
    ) # type: ignore

    tail_direction: bpy.props.EnumProperty(
            name="Tail Direction",
            description="Direction the bone tail should point",
            items=[
                ('+X', "+X", ""),
                ('-X', "-X", ""),
                ('+Y', "+Y", ""),
                ('-Y', "-Y", ""),
                ('+Z', "+Z", ""),
                ('-Z', "-Z", "")
            ],
            default='+Z'
        ) # type: ignore
    tail_length: bpy.props.FloatProperty(
        name="Tail Length",
        description="Length of the bone tail",
        default=1.0,
        min=0.0
    ) # type: ignore
    use_deform: bpy.props.BoolProperty(name="Use Deform", default=True) # type: ignore



    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.mode == 'EDIT' and obj.parent and obj.parent.type == 'ARMATURE'
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        mesh_obj = context.active_object

        armature_obj = mesh_obj.parent
        if not armature_obj or armature_obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Mesh must be parented to an armature")
            return {'CANCELLED'}

        # Get selected vertex positions
        bm = bmesh.from_edit_mesh(mesh_obj.data)
        selected_world_verts = [mesh_obj.matrix_world @ v.co for v in bm.verts if v.select]
        if not selected_world_verts:
            self.report({'ERROR'}, "No vertices selected")
            return {'CANCELLED'}

        center_world = sum(selected_world_verts, Vector()) / len(selected_world_verts)

        # Convert world space to armature edit space
        center = armature_obj.matrix_world.inverted() @ center_world

        # Switch to edit armature
        bpy.ops.object.mode_set(mode='OBJECT')
        context.view_layer.objects.active = armature_obj
        bpy.ops.object.mode_set(mode='EDIT')

        arm = armature_obj.data
        new_bone = arm.edit_bones.new(self.bone_name)
        new_bone.head = center

        direction_map = {
                    '+X': Vector((self.tail_length, 0, 0)),
                    '-X': Vector((-self.tail_length, 0, 0)),
                    '+Y': Vector((0, self.tail_length, 0)),
                    '-Y': Vector((0, -self.tail_length, 0)),
                    '+Z': Vector((0, 0, self.tail_length)),
                    '-Z': Vector((0, 0, -self.tail_length)),
                }
        direction_vector = direction_map[self.tail_direction]
        new_bone.tail = center + direction_vector
        new_bone.use_deform = self.use_deform

        bpy.ops.object.mode_set(mode='OBJECT')
        #context.view_layer.update()
        #bpy.ops.object.mode_set(mode='OBJECT')
        context.view_layer.objects.active = mesh_obj
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

def menu_func(self, context):
    ob = context.active_object
    if ob and ob.type == 'MESH' and ob.parent and ob.parent.type == 'ARMATURE' and ob.mode == 'EDIT':
        self.layout.operator(
            OBJECT_OT_johnnygizmo_add_bone_at_selected.bl_idname,
            text="Add Bone at Selected"
        )


def register():
    bpy.utils.register_class(OBJECT_OT_johnnygizmo_add_bone_at_selected)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_OT_johnnygizmo_add_bone_at_selected)
