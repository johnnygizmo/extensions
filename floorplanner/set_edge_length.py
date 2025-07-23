from bpy.types import Operator # type: ignore
import mathutils # type: ignore
from bpy.props import FloatProperty # type: ignore
import bpy # type: ignore


class JMFLOORPLANNER_OT_johnnygizmo_floorplanner_SetEdgeLength(bpy.types.Operator):
    bl_idname = 'jm_floorplanner.set_edge_length'
    bl_label = "Set Edge Length"
    bl_options = {'UNDO'}

    length: FloatProperty(name="Length", default=   5)  # type: ignore

    def execute(self, context):
        obj = context.object
        if obj and obj.type == 'MESH':
            bpy.ops.object.mode_set(mode='OBJECT')
            mesh = obj.data
            i = 0
            for e in mesh.edges:
                if e.select:

                    vec1 = mathutils.Vector(mesh.vertices[e.vertices[0]].co)
                    vec2 = mathutils.Vector(mesh.vertices[e.vertices[1]].co)

                    vec = vec2-vec1
                    length = vec.length
                    center = vec1.lerp(vec2, .5)

                    side1 = (vec1-center).normalized() * (self.length/2)
                    side2 = (vec2-center).normalized() * (self.length/2)

                    mesh.vertices[e.vertices[0]].co = center+side1
                    mesh.vertices[e.vertices[1]].co = center+side2

                i = i + 1

            bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}
    

def register():
    bpy.utils.register_class(JMFLOORPLANNER_OT_johnnygizmo_floorplanner_SetEdgeLength)


def unregister():
    bpy.utils.unregister_class(JMFLOORPLANNER_OT_johnnygizmo_floorplanner_SetEdgeLength)
