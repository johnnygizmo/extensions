bl_info = {
    "name": "New Vertex Child Empty",
    "blender": (4, 0, 0),
    "category": "Object",
    "version": (1, 0, 0),
    "author": "Your Name",
    "description": "Creates an empty parented to each selected vertex.",
    "location": "Search Menu",
}

import bpy
import bmesh

class NEW_OT_vertex_child_empty(bpy.types.Operator):
    """Creates an empty parented to each selected vertex."""
    bl_idname = "object.new_vertex_child_empty"
    bl_label = "New Vertex Child Empty"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "Active object is not a mesh")
            return {'CANCELLED'}

        # Get selected vertices in edit mode
        bpy.ops.object.mode_set(mode='OBJECT')
        mesh = obj.data
        selected_verts = [v for v in mesh.vertices if v.select]

        if not selected_verts:
            self.report({'ERROR'}, "No vertices selected")
            return {'CANCELLED'}

        empties = []
        for vert in selected_verts:
            empty = bpy.data.objects.new(name="Vertex_Empty", object_data=None)
            empty.location = obj.matrix_world @ vert.co  # Convert local to world space
            bpy.context.collection.objects.link(empty)
            empty.parent = obj
            empty.parent_type = 'VERTEX'
            empty.parent_vertices = ([vert.index,vert.index,vert.index])
            empties.append(empty)
            bpy.ops.object.origin_clear()

        bpy.ops.object.select_all(action='DESELECT')
        for empty in empties:
            empty.select_set(True)
        bpy.ops.object.origin_clear()
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj


        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

# Register the operator
def menu_func(self, context):
    self.layout.operator(NEW_OT_vertex_child_empty.bl_idname, text=NEW_OT_vertex_child_empty.bl_label)

def register():
    bpy.utils.register_class(NEW_OT_vertex_child_empty)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(NEW_OT_vertex_child_empty)

if __name__ == "__main__":
    register()