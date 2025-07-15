import bpy  # type: ignore
from . import color_utils
from . import harmony_settings
from . import lib_custom_palette

class COLORHARMONY_PT_material_panel(bpy.types.Panel):
    bl_label = "Color Harmony Tools"
    bl_idname = "COLORHARMONY_PT_material_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.johnnygizmo_harmony

        obj = context.active_object
        mat = obj.active_material if obj else None

        if mat and mat.use_nodes:
            row = layout.row()
            # filter the prop_search to only show BSDF nodes

            row.prop(props, "base_color", text="")

        row = layout.row()
        row.prop(props, "mode", text="")
        if props.mode in {"analogous", "analogous_c"}:
            row.prop(props, "count", text="Amt")
            row.prop(props, "analogous_angle", text="Angle")
            # if props.count % 2 == 0:
            #     layout.label(text="Count must be odd, adjusting")

        if props.mode in {"near_complementary"}:
            row.prop(props, "near_complementary_angle", text="Angle")

        if props.mode in {"monochromatic"}:
            layout.prop(props, "count", text="Steps")

        if props.mode == "achromatic":
            layout.prop(props, "count", text="Steps")

        if props.mode == "tint_shade":
            layout.prop(props, "count", text="Steps")

        if props.mode == "tetradic":
            layout.prop(props, "tetradic_angle", text="Angle")

        # Display the palette assigned to this scene
        palette = props.palette
        row = layout.row()
        column = row.column(align=True)
        if palette:
            lib_custom_palette.color_palette(column, palette, props.mode, props.count)
        else:
            column.label(text="No palette assigned.")

        layout.separator(type='LINE')
        if mat and mat.use_nodes:
            if mat.node_tree and mat.node_tree.nodes.get(props.target_bsdf_node_name):
                # layout.label(text="Apply to: " + props.target_bsdf_node_name)
                bsdf_node = mat.node_tree.nodes.get(props.target_bsdf_node_name)
                if bsdf_node.type == "BSDF_PRINCIPLED":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Color",
                    ).input = "Base Color"
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Spec",
                    ).input = "Specular Tint"
                    # row = layout.row(align=True)
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Emit",
                    ).input = "Emission Color"
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Coat",
                    ).input = "Coat Tint"
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Sheen",
                    ).input = "Sheen Tint"
                elif bsdf_node.type == "EMISSION":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Color",
                    ).input = "Color"
                elif bsdf_node.type == "EEVEE_SPECULAR":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Color",
                    ).input = "Base Color"
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Spec",
                    ).input = "Specular"
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Emit",
                    ).input = "Emissive Color"
                elif bsdf_node.type == "BSDF_TRANSPARENT":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Color",
                    ).input = "Color"
                elif bsdf_node.type == "BSDF_METALLIC":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Color",
                    ).input = "Base Color"
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Edge",
                    ).input = "Edge Tint"
                elif bsdf_node.type == "BSDF_DIFFUSE":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Color",
                    ).input = "Color"
                elif bsdf_node.type == "BSDF_GLASS":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Color",
                    ).input = "Color"
                elif bsdf_node.type == "BSDF_REFRACTION":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Color",
                    ).input = "Color"
                elif bsdf_node.type == "BSDF_GLOSSY":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Color",
                    ).input = "Color"
                elif bsdf_node.type == "BSDF_TRANSLUCENT":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Color",
                    ).input = "Color"
                elif bsdf_node.type == "VOLUME_ABSORPTION":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Color",
                    ).input = "Color"
                elif bsdf_node.type == "PRINCIPLED_VOLUME":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Color",
                    ).input = "Color"
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Absorption",
                    ).input = "Absorption Color"
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Emit",
                    ).input = "Emission Color"
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Blackbody",
                    ).input = "Blackbody Tint"
                elif bsdf_node.type == "VOLUME_SCATTER":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Color",
                    ).input = "Color"
                elif bsdf_node.type == "SUBSURFACE_SCATTERING":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Color",
                    ).input = "Color"
                elif bsdf_node.type == "BSDF_SHEEN":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Color",
                    ).input = "Color"
                elif bsdf_node.type == "BSDF_TOON":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Color",
                    ).input = "Color"
                elif bsdf_node.type == "BSDF_RAY_PORTAL":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Color",
                    ).input = "Color"
                elif bsdf_node.type == "BSDF_HAIR_PRINCIPLED":
                    row = layout.row(align=True)
                    row.label(text="Set:")
                    if bsdf_node.parametrization == "COLOR":
                        row.operator(
                            "johnnygizmo_colorharmony.apply_selected_palette_color",
                            text="Color",
                        ).input = "Color"
                    elif bsdf_node.parametrization == "MELANIN":
                        row.operator(
                            "johnnygizmo_colorharmony.apply_selected_palette_color",
                            text="Tint",
                        ).input = "Tint"


           
            row = layout.row()
            split = row.split(factor=0.5)
            split.prop(
                props,
                "target_bsdf_node_name",
                text="",
                icon="NODE",
            )
            right = split.split(factor=0.5)
            right.operator("johnnygizmo_colorharmony.get_node", text="Get Node")
            
            right.operator(
                "johnnygizmo_colorharmony.get_base_palette_color", text="Get Color"
            )

            (head,body) = layout.panel("Tools",default_closed=True)
            head.label(text="Harmony Copy Tools")
            if body:   
                row = body.row() 
                row.label(text="Palette")
                op = row.operator(
                    "johnnygizmo_colorharmony.save_palette_copy", text="Copy To Palette"
                )              
                result = next((item for item in harmony_settings.HARMONY_TYPES if item[0] == props.mode), None)
                op.new_name = (
                    result[1]
                    + " Palette: [ "
                    + str(round(props.base_color[0],3)) + ", "
                    + str(round(props.base_color[1],3)) + ", "
                    + str(round(props.base_color[2],3))
                    + " ]"
                )
                row = body.row() 
                row.label(text="Color Ramp")
                op =row.operator(
                                "johnnygizmo_colorharmony.palette_color_to_rgb_node",
                                text="Linear",
                            )
                op.mode = "CREATECOLORRAMP"
                op.spacing = False
                op =row.operator(
                                "johnnygizmo_colorharmony.palette_color_to_rgb_node",
                                text="Constant",
                            )
                op.mode = "CREATECOLORRAMP"
                op.spacing = True

                newrow = body.row()
                newrow.label(text="RGB Nodes")
                newrow.operator(
                                "johnnygizmo_colorharmony.palette_color_to_rgb_node",
                                text="Selected Color",
                            ).mode = "CREATERGBNODE" 
                newrow.operator(
                                "johnnygizmo_colorharmony.palette_color_to_rgb_node",
                                text="All Colors",
                            ).mode = "CREATERGBNODES"            
