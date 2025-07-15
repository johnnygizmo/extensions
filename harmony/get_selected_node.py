import bpy  # type: ignore
from bpy.props import FloatVectorProperty, PointerProperty  # type: ignore
from math import pow  # Ensure pow is imported
from . import lib_assign

class JOHNNYGIZMO_COLORHARMONY_OT_GetSelectedNode(bpy.types.Operator):
    """Get the active Node BSDF"""

    bl_idname = "johnnygizmo_colorharmony.get_node"
    bl_label = "Get Node"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        props = context.scene.johnnygizmo_harmony
        obj = context.object

        if not obj:
            self.report({"WARNING"}, "No active object selected.")
            return {"CANCELLED"}

        if obj.type == "LIGHT":
            mat = obj.data

            if not mat.use_nodes:
                self.report({"WARNING"}, "Light does not use nodes.")
                return {"CANCELLED"}
            lib_assign.setNode(mat, props)

        else:
            mat = obj.active_material

            if not mat:
                self.report({"WARNING"}, "Active object has no material.")
                return {"CANCELLED"}

            if not mat.use_nodes:
                self.report({"WARNING"}, "Material does not use nodes.")
                return {"CANCELLED"}
            lib_assign.setNode(mat, props)
        return {"FINISHED"}
