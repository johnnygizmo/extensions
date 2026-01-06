import bpy # type: ignore
import bmesh # type: ignore
from mathutils import Vector # type: ignore

class MESH_OT_johnnygizmo_create_rig_and_assign(bpy.types.Operator):
    bl_idname = "mesh.johnnygizmo_create_rig_and_assign"
    bl_label = "Create Armature and Assign Bone"
    bl_options = {'REGISTER', 'UNDO'}

    number_of_bones: bpy.props.IntProperty(
        name="Number of Bones",
        description="Number of bones to create in the armature",
        default=1,
        min=1,
        max=100,
    )  # type: ignore

    parent_type: bpy.props.EnumProperty(
        name="Parenting Method",
        description="Choose how to assign the mesh to the armature",
        items=[
            ('BONE', "Bone", "Parent to the bone"),
            ('ARMATURE', "Armature", "Parent to the armature object for vertex groups"),           
            ('OBJECT', "Object", "Parent to the armature object without bone influence"),
        ],
        default='ARMATURE',
    )  # type: ignore

    def execute(self, context):

        if context.mode != 'EDIT_MESH':
            #Toggle edit mode
            bpy.ops.object.mode_set(mode='EDIT')
            #select all vertices
            bpy.ops.mesh.select_all(action='SELECT')
        mesh_obj = context.edit_object
        if mesh_obj.type != 'MESH':
            self.report({'WARNING'}, "Active object must be a mesh.")
            return {'CANCELLED'}

        if mesh_obj.parent:
            self.report({'WARNING'}, "Mesh already has a parent.")
            return {'CANCELLED'}

        bm = bmesh.from_edit_mesh(mesh_obj.data)
        selected = [v.co for v in bm.verts if v.select]
        if not selected:
            self.report({'WARNING'}, "No vertices selected.")
            return {'CANCELLED'}

        # Compute center of selection in world space
        center_local = sum(selected, Vector()) / len(selected)
        center_world = mesh_obj.matrix_world @ center_local

        bpy.ops.object.mode_set(mode='OBJECT')

        # Create the new armature object
        arm_data = bpy.data.armatures.new(mesh_obj.name + "_Rig")
        arm_obj = bpy.data.objects.new(mesh_obj.name + "_Armature", arm_data)
        arm_obj.location = center_world
        bpy.context.collection.objects.link(arm_obj)

        # Create a single bone at the armature origin
        bpy.context.view_layer.objects.active = arm_obj
        bpy.ops.object.mode_set(mode='EDIT')
        prev_bone = None
        for i in range(self.number_of_bones):
            bone = arm_data.edit_bones.new("Bone")
           
            bone.head = Vector((0, 0, i))
            bone.tail = Vector((0, 0, i+1))
            if i > 0 and prev_bone:
                bone.parent = prev_bone
                bone.use_connect = True
            if i == 0:
                arm_data.edit_bones.active = bone
                bone.select = True
            
            prev_bone = bone

        bpy.ops.object.mode_set(mode='OBJECT')

        original_matrix = mesh_obj.matrix_world.copy()

       # Deselect all, then select both
        bpy.ops.object.select_all(action='DESELECT')
        mesh_obj.select_set(True)
        arm_obj.select_set(True)
        bpy.context.view_layer.objects.active = arm_obj

        if self.parent_type == 'OBJECT':
            # Keep transform manually since Blender has no OBJECT option in ops
            original_matrix = mesh_obj.matrix_world.copy()
            mesh_obj.parent = arm_obj
            mesh_obj.parent_type = 'OBJECT'
            mesh_obj.matrix_world = original_matrix

        elif self.parent_type == 'ARMATURE':
            bpy.ops.object.parent_set(type='ARMATURE')

        elif self.parent_type == 'BONE':

            bpy.ops.object.parent_set(type='BONE', keep_transform=True)

        self.report({'INFO'}, "Armature created and assigned at selection center.")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Assign Mesh to Armature:")
        layout.prop(self, "parent_type", expand=True)
        layout.prop(self, "number_of_bones", text="Number of Bones")

def menu_func(self, context):
    self.layout.operator(MESH_OT_johnnygizmo_create_rig_and_assign.bl_idname)

def register():
    bpy.utils.register_class(MESH_OT_johnnygizmo_create_rig_and_assign)
    bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)
    bpy.utils.unregister_class(MESH_OT_johnnygizmo_create_rig_and_assign)
