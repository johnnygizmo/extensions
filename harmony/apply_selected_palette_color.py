import bpy  # type: ignore
#from bpy.props import FloatVectorProperty, PointerProperty  # type: ignore
from math import pow  # Ensure pow is imported
from . import color_utils
from . import lib_assign

class JOHNNYGIZMO_COLORHARMONY_OT_ApplySelectedPaletteColor(bpy.types.Operator):
    """Assign Colors to Node Sockets"""

    bl_idname = "johnnygizmo_colorharmony.apply_selected_palette_color"
    bl_label = "Apply Selected Palette Color"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    input: bpy.props.StringProperty(
        name="Input",
        description="Input name to apply the color to",
        default="Base Color",
    )  # type: ignore

    obtype: bpy.props.EnumProperty(
        name="Type",
        description="Type of input to apply the color to",
        items=[
            ("MATERIAL", "Material", "Apply to Material"),
            ("LIGHT", "Light", "Apply to Light"),
        ],
        default="MATERIAL",
    )  # type: ignore

    def execute(self, context):
        props = context.scene.johnnygizmo_harmony
        selected_color = props.palette.colors.active.color
        srgb_color = color_utils.convert_srgb_to_linear_rgb(selected_color[:3])
        ob = context.active_object

        if ob.type == "LIGHT":
            light = ob.data
            if self.input == "light_color":
                light.color = srgb_color
            elif self.input == "LightEmmissionColor":
                bsdf = ob.data.node_tree.nodes.get(props.target_bsdf_node_name)
                bsdf.inputs["Color"].default_value = (*srgb_color, 1.0)
                light.color = [1,1,1]
                light.use_temperature = False
                self.report({'INFO'}, f"Note: Light base color set to white, and Temperature turned off")
            return {"FINISHED"}

        for obj in context.selected_objects:
            (node_material, obj, mat) = lib_assign.checkObMat(self, context, obj)
            if not node_material:
                continue

            bsdf = mat.node_tree.nodes.get(props.target_bsdf_node_name)
            if not bsdf:
                continue

            palette = props.palette
            if not palette:
                continue

            if palette.colors.active:
                selected_color = palette.colors.active.color
                srgb_color = color_utils.convert_srgb_to_linear_rgb(selected_color[:3])

                if self.input == "Color" or self.input == "Base Color":
                    mat.diffuse_color = (*srgb_color[:3], 1.0)

                bsdf.inputs[self.input].default_value = (*srgb_color, 1.0)
            else:
                self.report(
                    {"WARNING"}, "No active color selected in the Harmony Palette."
                )
                return {"CANCELLED"}

        return {"FINISHED"}
