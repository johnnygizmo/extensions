import bpy  # type: ignore
from bpy.props import FloatVectorProperty, PointerProperty  # type: ignore
from math import pow,inf  # Ensure pow is imported
from . import color_utils
from . import harmony_settings
from . import lib_assign


def node_bounds(nodetree):
    min_x = inf
    min_y = inf
    max_x = -inf
    max_y = -inf

    for node in nodetree.nodes:
        print(node.location, node.name)
        if node.location[0] - node.width/2 < min_x:
            min_x = node.location[0] - node.width/2
        if node.location[0] + node.width/2 > max_x:
            max_x = node.location[0] + node.width/2        
        if node.location[0] - node.height/2 < min_y:
            min_y = node.location[0] - node.width/2
        if node.location[0] + node.height/2 > max_y:
            max_y = node.location[0] + node.width/2 
    if not nodetree.nodes or len(nodetree.nodes) == 0:
        return ([0,0],[0,0])
    return ([min_x,min_y],[max_x,max_y])

class JOHNNYGIZMO_COLORHARMONY_OT_PaletteColorToRGBNodes(bpy.types.Operator):
    """Create RGB Nodes in the active Material"""

    bl_idname = "johnnygizmo_colorharmony.palette_color_to_rgb_node"
    bl_label = "Create RGB Node"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    mode: bpy.props.StringProperty(
        name="Mode", description="Execution Mode", default="CREATERGBNODE"
    )  # type: ignore
    spacing: bpy.props.BoolProperty(
        name="spacing",
        description="If ColorRamp should be spaced with extra space",
        default=False,
    )  # type: ignore

    def execute(self, context):
        props = context.scene.johnnygizmo_harmony
        obj = context.active_object

        (node_material, obj, mat) = lib_assign.checkObMat(self, context, obj)
        if not node_material:
            return {"CANCELLED"}

        palette = props.palette
        if not palette:
            return {"CANCELLED"}
        harmony_mode = next(
            item for item in harmony_settings.HARMONY_TYPES if item[0] == props.mode
        )[1]

        if self.mode == "CREATERGBNODE":

            selected_color = palette.colors.active.color
            srgb_color = color_utils.convert_srgb_to_linear_rgb(selected_color[:3])
            nodes = mat.node_tree.nodes
            for node in nodes:
                node.select = False
            rgb_node = nodes.new(type="ShaderNodeRGB")

            rgb_node.label = (
                color_utils.color_to_string(srgb_color)
                # + " : "
                # + color_utils.color_to_hex(srgb_color)
            )
            rgb_node.name = "Harmony"  # This sets the actual ID name
            (min,max) = node_bounds(mat.node_tree)
            rgb_node.location = (min[0]-250,max[1]-150)
            rgb_node.outputs[0].default_value = (*selected_color[:3], 1.0)  # RGBA
            rgb_node.select = False
            new_name = (
                harmony_mode
                + " : "
                + color_utils.color_to_string(props.base_color)
                # + " - "
                # + color_utils.color_to_hex(props.base_color)
            )

            frame = nodes.new(type="NodeFrame")
            frame.label = new_name  # Optional: label same as RGB node
            frame.name = "Harmony Frame"
            frame.location = (rgb_node.location[0] - 20, rgb_node.location[1] - 20)
            frame.width = 140  # Optional: default width for visual organization
            frame.height = 100  # Optional: you can adjust this if needed

            # Parent the RGB node to the frame
            rgb_node.parent = frame
            frame.select = True
        elif self.mode == "CREATERGBNODES":
            nodes = mat.node_tree.nodes
            for node in nodes:
                node.select = False
            new_name = (
                harmony_mode
                + " : "
                + color_utils.color_to_string(props.base_color)
                # + " - "
                # + color_utils.color_to_hex(props.base_color)
            )

            (min,max) = node_bounds(mat.node_tree)
            loc = (min[0]-250,max[1]-150)

            frame = nodes.new(type="NodeFrame")
            frame.label = new_name  # Optional: label same as RGB node
            frame.name = "Harmony Frame"
            frame.location = loc
            frame.width = 140  # Optional: default width for visual organization
            frame.height = 100
            frame.select = True

            for idx in range(0, len(palette.colors)):
                rgb_node = nodes.new(type="ShaderNodeRGB")
                srgb_color = color_utils.convert_srgb_to_linear_rgb(
                    palette.colors[idx].color[:3]
                )
                new_name = (
                    props.mode
                    + " [ "
                    + str(round(props.base_color[0], 3))
                    + ", "
                    + str(round(props.base_color[1], 3))
                    + ", "
                    + str(round(props.base_color[2], 3))
                    + " ] : "
                    + str(idx)
                )

                rgb_node.label = (
                    color_utils.color_to_string(srgb_color)
                    # + " - "
                    # + color_utils.color_to_hex(srgb_color)
                    + " : "
                    + str(idx)
                )

                rgb_node.name = "Harmony"  # This sets the actual ID name
                rgb_node.location = (loc[0]+5, (loc[1]-5)-idx * 200)

                rgb_node.outputs[0].default_value = (*srgb_color[:3], 1.0)
                rgb_node.parent = frame
                rgb_node.select = False

        elif self.mode == "CREATECOLORRAMP":

            nodes = mat.node_tree.nodes
            for node in nodes:
                node.select = False
            new_name = (
                harmony_mode
                + " : "
                + color_utils.color_to_string(props.base_color)
                # + " - "
                # + color_utils.color_to_hex(props.base_color)
            )

            frame = nodes.new(type="NodeFrame")
            frame.label = new_name  # Optional: label same as RGB node
            frame.name = "Harmony Frame"
            (min,max) = node_bounds(mat.node_tree)
            loc = (min[0]-250,max[1]-250)
            frame.location = loc
            frame.width = 140  # Optional: default width for visual organization
            frame.height = 100
            frame.select = True

            # Create ColorRamp node
            ramp_node = nodes.new(type="ShaderNodeValToRGB")
            ramp_node.location = loc
            ramp_node.label = "Harmony Ramp"
            ramp_node.name = "HarmonyRamp"

            if self.spacing:
                ramp_node.color_ramp.interpolation = "CONSTANT"
            else:
                ramp_node.color_ramp.interpolation = "LINEAR"

            # Ensure at least one default element remains
            while len(ramp_node.color_ramp.elements) > 1:
                ramp_node.color_ramp.elements.remove(ramp_node.color_ramp.elements[0])

            # Reuse the first element
            first_element = ramp_node.color_ramp.elements[0]
            first_element.position = 0.0
            first_element.color = (*props.palette.colors[0].color, 1.0)

            # Add the rest of the colors
            count = len(props.palette.colors)
            for i, col in enumerate(props.palette.colors[1:], start=1):
                extra = 1
                if self.spacing == True:
                    extra = 0

                pos = i / (count - extra)
                el = ramp_node.color_ramp.elements.new(pos)
                el.color = (*col.color, 1.0)

            ramp_node.parent = frame
        else:
            self.report({"WARNING"}, "No active color selected in the Harmony Palette.")
            return {"CANCELLED"}

        self.report(
            {"INFO"}, f"See Shader Node Tree for Material '" + mat.name + "' New Nodes"
        )

        return {"FINISHED"}

