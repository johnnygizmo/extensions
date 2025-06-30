import bpy # type: ignore
import bmesh # type: ignore
from mathutils import Vector # type: ignore

class OBJECT_OT_parent_meshes_to_nearest_bone(bpy.types.Operator):
    """Parent selected mesh objects to nearest bone of active armature"""
    bl_idname = "object.parent_meshes_to_nearest_bone"
    bl_label = "Parent Meshes to Nearest Bone"
    bl_options = {'REGISTER', 'UNDO'}

    bone_point: bpy.props.EnumProperty(
        name="Bone Point",
        description="Which part of the bone to use for proximity",
        items=[
            ('HEAD', "Head", "Use the bone's head position"),
            ('TAIL', "Tail", "Use the bone's tail position"),
            ('CENTER', "Center", "Use the midpoint of the bone")
        ],
        default='CENTER'
    ) # type: ignore
    only_deform: bpy.props.BoolProperty(
        name="Use Deform",
        description="Use deform bone parenting",
        default=True
    ) # type: ignore
    replace_parent: bpy.props.BoolProperty(
        name="Replace Parent",
        description="Replace existing parent with armature",
        default=False
    ) # type: ignore

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def execute(self, context):
        selected_objects = context.selected_objects
        active_obj = context.active_object

        if not active_obj or active_obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Active object must be an armature")
            return {'CANCELLED'}

        armature = active_obj
        mesh_objects = [obj for obj in selected_objects if obj.type == 'MESH' and obj != armature]


        if not mesh_objects:
            self.report({'ERROR'}, "No unparented mesh objects selected")
            return {'CANCELLED'}

        for mesh_obj in mesh_objects:
            if mesh_obj.parent and self.replace_parent is False:
                self.report({'ERROR'}, f"{mesh_obj.name} is already parented")
                continue
            avg_loc = self.get_average_vertex_location(mesh_obj)
            nearest_bone_name = self.find_nearest_bone(armature, avg_loc)

            if nearest_bone_name:
                bpy.ops.object.select_all(action='DESELECT')
                mesh_obj.select_set(True)
                context.view_layer.objects.active = mesh_obj

                # FIX: Preserve transform when parenting
                world_matrix = mesh_obj.matrix_world.copy()
                mesh_obj.parent = armature
                mesh_obj.parent_type = 'BONE'
                mesh_obj.parent_bone = nearest_bone_name
                mesh_obj.matrix_world = world_matrix

                self.report({'INFO'}, f"Parented {mesh_obj.name} to {nearest_bone_name}")
            else:
                self.report({'WARNING'}, f"No nearby bone found for {mesh_obj.name}")

        return {'FINISHED'}

    def get_average_vertex_location(self, obj):
        depsgraph = bpy.context.evaluated_depsgraph_get()
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.to_mesh()

        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.verts.ensure_lookup_table()

        total = Vector((0, 0, 0))
        for vert in bm.verts:
            total += obj.matrix_world @ vert.co
        avg = total / len(bm.verts)

        bm.free()
        eval_obj.to_mesh_clear()

        return avg

    def find_nearest_bone(self, armature, location_world):
        min_distance = float('inf')
        nearest_bone_name = None

        for bone in armature.data.bones:
            if self.only_deform and bone.use_deform is False:
                continue
            if self.bone_point == 'HEAD':
                point = bone.head_local
            elif self.bone_point == 'TAIL':
                point = bone.tail_local
            else:  # CENTER
                point = (bone.head_local + bone.tail_local) / 2

            bone_point_world = armature.matrix_world @ point
            dist = (location_world - bone_point_world).length

            if dist < min_distance:
                min_distance = dist
                nearest_bone_name = bone.name

        return nearest_bone_name

def register():
    bpy.utils.register_class(OBJECT_OT_parent_meshes_to_nearest_bone)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_parent_meshes_to_nearest_bone)
