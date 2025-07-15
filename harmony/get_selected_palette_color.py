import bpy  # type: ignore
from bpy.props import FloatVectorProperty, PointerProperty  # type: ignore
from math import pow  # Ensure pow is imported
from . import harmony_settings
from . import lib_assign

class JOHNNYGIZMO_COLORHARMONY_OT_GetSelectedPaletteColor(bpy.types.Operator):
    """Get the active material's Base Color and set Base Color"""

    bl_idname = "johnnygizmo_colorharmony.get_base_palette_color"
    bl_label = "Get Base Palette Color"
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

        mat = obj.data if obj.type == "LIGHT" else obj.active_material

        if not mat:
            self.report({"WARNING"}, "Active object has no material.")
            return {"CANCELLED"}

        if not mat.use_nodes:
            self.report({"WARNING"}, "Material does not use nodes.")
            return {"CANCELLED"}

        lib_assign.setNode(mat, props)

        if mat.node_tree.nodes.get(props.target_bsdf_node_name) is None:
            props.target_bsdf_node_name = ""
        elif (
            mat.node_tree.nodes.get(props.target_bsdf_node_name).type
            not in harmony_settings.type_list
        ):
            props.target_bsdf_node_name = ""

        if not props.target_bsdf_node_name:
            for node in mat.node_tree.nodes:
                if node.type in harmony_settings.type_list:
                    props.target_bsdf_node_name = node.name
                    break

        bsdf = mat.node_tree.nodes.get(props.target_bsdf_node_name)

        if not bsdf:
            self.report({"WARNING"}, "Selected node not found in material.")
            return {"CANCELLED"}

        palette = bpy.data.palettes.get("Harmony Palette")
        if not palette:
            self.report(
                {"WARNING"}, "Harmony Palette not found. Please generate colors first."
            )
            return {"CANCELLED"}

        if bsdf.inputs.get("Base Color") is not None:
            props.base_color = bsdf.inputs["Base Color"].default_value
        elif bsdf.inputs.get("Color") is not None:
            props.base_color = bsdf.inputs["Color"].default_value

        return {"FINISHED"}