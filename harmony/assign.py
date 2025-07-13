import bpy  # type: ignore
from bpy.props import FloatVectorProperty, PointerProperty  # type: ignore
from math import pow  # Ensure pow is imported
from . import color_utils
from . import harmony_colors


def setNode(mat, props):
    if mat.node_tree.nodes.get(props.target_bsdf_node_name) is None:
        props.target_bsdf_node_name = ""
    elif (
        mat.node_tree.nodes.get(props.target_bsdf_node_name).type
        not in harmony_colors.type_list
    ):
        props.target_bsdf_node_name = ""

    if not props.target_bsdf_node_name:
        for node in mat.node_tree.nodes:
            if node.type in harmony_colors.type_list:
                props.target_bsdf_node_name = node.name
                break


def checkObMat(self, context, obj):
    if not obj:
        self.report({"WARNING"}, "No active object selected.")
        return (False, None, None)

    mat = obj.active_material
    if not mat:
        self.report({"WARNING"}, obj.name + " has no active material.")
        return (False, obj, None)
    if not mat.use_nodes:
        self.report({"WARNING"}, "Material on " + obj.name + " does not use nodes.")
        return (False, obj, mat)
    return (True, obj, mat)


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

    def execute(self, context):
        props = context.scene.johnnygizmo_harmony
        for obj in context.selected_objects:
            (node_material, obj, mat) = checkObMat(self, context, obj)
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
    ) # type: ignore

    def execute(self, context):
        props = context.scene.johnnygizmo_harmony
        obj = context.active_object

        (node_material, obj, mat) = checkObMat(self, context, obj)
        if not node_material:
            return

        bsdf = mat.node_tree.nodes.get(props.target_bsdf_node_name)
        if not bsdf:
            return

        palette = props.palette
        if not palette:
            return

        harmony_mode = next(
            item for item in harmony_colors.HARMONY_TYPES if item[0] == props.mode
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
            rgb_node.location = (200, 200)
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

            frame = nodes.new(type="NodeFrame")
            frame.label = new_name  # Optional: label same as RGB node
            frame.name = "Harmony Frame"
            frame.location = (100, 100)
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
                rgb_node.location = (0, -idx * 200)

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
            frame.location = (100, 100)
            frame.width = 140  # Optional: default width for visual organization
            frame.height = 100
            frame.select = True

            # Create ColorRamp node
            ramp_node = nodes.new(type="ShaderNodeValToRGB")
            ramp_node.location = (125, 125)
            ramp_node.label = "Harmony Ramp"
            ramp_node.name = "HarmonyRamp"

            if self.spacing:
                ramp_node.color_ramp.interpolation = 'CONSTANT'
            else:
                ramp_node.color_ramp.interpolation = 'LINEAR'
                

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
        
        self.report({'INFO'}, f"See Shader Node Tree for Material '"+ mat.name +"' New Nodes")
        
        return {"FINISHED"}


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

        mat = obj.active_material

        if not mat:
            self.report({"WARNING"}, "Active object has no material.")
            return {"CANCELLED"}

        if not mat.use_nodes:
            self.report({"WARNING"}, "Material does not use nodes.")
            return {"CANCELLED"}

        setNode(mat, props)

        if mat.node_tree.nodes.get(props.target_bsdf_node_name) is None:
            props.target_bsdf_node_name = ""
        elif (
            mat.node_tree.nodes.get(props.target_bsdf_node_name).type
            not in harmony_colors.type_list
        ):
            props.target_bsdf_node_name = ""

        if not props.target_bsdf_node_name:
            for node in mat.node_tree.nodes:
                if node.type in harmony_colors.type_list:
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

        mat = obj.active_material

        if not mat:
            self.report({"WARNING"}, "Active object has no material.")
            return {"CANCELLED"}

        if not mat.use_nodes:
            self.report({"WARNING"}, "Material does not use nodes.")
            return {"CANCELLED"}
        setNode(mat, props)
        return {"FINISHED"}


def register():
    bpy.utils.register_class(JOHNNYGIZMO_COLORHARMONY_OT_ApplySelectedPaletteColor)
    bpy.utils.register_class(JOHNNYGIZMO_COLORHARMONY_OT_GetSelectedPaletteColor)
    bpy.utils.register_class(JOHNNYGIZMO_COLORHARMONY_OT_GetSelectedNode)
    bpy.utils.register_class(JOHNNYGIZMO_COLORHARMONY_OT_PaletteColorToRGBNodes)


def unregister():
    bpy.utils.unregister_class(JOHNNYGIZMO_COLORHARMONY_OT_ApplySelectedPaletteColor)
    bpy.utils.unregister_class(JOHNNYGIZMO_COLORHARMONY_OT_GetSelectedPaletteColor)
    bpy.utils.unregister_class(JOHNNYGIZMO_COLORHARMONY_OT_GetSelectedNode)
    bpy.utils.unregister_class(JOHNNYGIZMO_COLORHARMONY_OT_PaletteColorToRGBNodes)
