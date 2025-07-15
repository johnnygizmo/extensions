
import bpy  # type: ignore
from . import lib_custom_palette
from . import harmony_settings

class COLORHARMONY_PT_Light_Panel(bpy.types.Panel):
    bl_label = "Color Harmony Tools"
    bl_idname = "COLORHARMONY_PT_light_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        engine = context.engine
        return context.light

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.johnnygizmo_harmony
        layout.label(text="Color Harmony Tools", icon="COLOR")

        obj = context.active_object
        # mat = obj.active_material if obj else None

        # if mat and mat.use_nodes:
        #     
        #     # filter the prop_search to only show BSDF nodes
        row = layout.row()
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

        if obj and obj.type == 'LIGHT':
           
            row = layout.row(align=True)
            row.label(text="Set:")
            if obj.data.node_tree and obj.data.node_tree.nodes.get(props.target_bsdf_node_name):
                bsdf_node = obj.data.node_tree.nodes[props.target_bsdf_node_name]
                if bsdf_node.type == "EMISSION":                    
                    row.operator(
                        "johnnygizmo_colorharmony.apply_selected_palette_color",
                        text="Node Color",
                    ).input = "LightEmmissionColor"
            op = row.operator(
                "johnnygizmo_colorharmony.apply_selected_palette_color",
                text="Light Base Color",
            )
            op.input = "light_color"
            op.obtype = "LIGHT"
            
           
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

def register():
    bpy.utils.register_class(COLORHARMONY_PT_Light_Panel)


def unregister():
    bpy.utils.unregister_class(COLORHARMONY_PT_Light_Panel)


