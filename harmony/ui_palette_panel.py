import bpy
from . import lib_custom_palette
from . import harmony_settings

class COLORHARMONY_PT_palette_panel(bpy.types.Panel):
    bl_label = "Harmony Palette"
    bl_idname = "COLORHARMONY_PT_paint_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Harmony Palette'

    @classmethod
    def poll(cls, context):
        mode = context.mode
        return mode in {'SCULPT', 'VERTEX_PAINT', 'TEXTURE_PAINT'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.johnnygizmo_harmony
       
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
            lib_custom_palette.color_palette(column, palette, props.mode, props.count, False)
        else:
            column.label(text="No palette assigned.")

        
        op = layout.operator(
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
        layout.separator(type='LINE')
        layout.label(text="Existing Palettes")       
        settings = self.paint_settings(self,context)

        layout.template_ID(settings, "palette", new="palette.new")
        if settings.palette:
            layout.template_palette(settings, "palette", color=True)
    
    @staticmethod
    def paint_settings(self,context):
        tool_settings = context.tool_settings

        mode = self.get_brush_mode(context)

        # 3D paint settings
        if mode == 'SCULPT':
            return tool_settings.sculpt
        elif mode == 'PAINT_VERTEX':
            return tool_settings.vertex_paint
        elif mode == 'PAINT_WEIGHT':
            return tool_settings.weight_paint
        elif mode == 'PAINT_TEXTURE':
            return tool_settings.image_paint
        elif mode == 'PARTICLE':
            return tool_settings.particle_edit
        # 2D paint settings
        elif mode == 'PAINT_2D':
            return tool_settings.image_paint
        # Grease Pencil settings
        elif mode == 'PAINT_GPENCIL':
            return tool_settings.gpencil_paint
        elif mode == 'SCULPT_GPENCIL':
            return tool_settings.gpencil_sculpt_paint
        elif mode == 'WEIGHT_GPENCIL':
            return tool_settings.gpencil_weight_paint
        elif mode == 'VERTEX_GPENCIL':
            return tool_settings.gpencil_vertex_paint
        elif mode == 'PAINT_GREASE_PENCIL':
            return tool_settings.gpencil_paint
        elif mode == 'SCULPT_CURVES':
            return tool_settings.curves_sculpt
        elif mode == 'PAINT_GREASE_PENCIL':
            return tool_settings.gpencil_paint
        elif mode == 'SCULPT_GREASE_PENCIL':
            return tool_settings.gpencil_sculpt_paint
        elif mode == 'WEIGHT_GREASE_PENCIL':
            return tool_settings.gpencil_weight_paint
        elif mode == 'VERTEX_GREASE_PENCIL':
            return tool_settings.gpencil_vertex_paint
        return None

    @staticmethod
    def get_brush_mode(context):
        """ Get the correct mode for this context. For any context where this returns None,
            no brush options should be displayed."""
        mode = context.mode

        if mode == 'PARTICLE':
            # Particle brush settings currently completely do their own thing.
            return None

        from bl_ui.space_toolsystem_common import ToolSelectPanelHelper
        tool = ToolSelectPanelHelper.tool_active_from_context(context)

        if not tool:
            # If there is no active tool, then there can't be an active brush.
            return None

        if not tool.use_brushes:
            return None

        space_data = context.space_data
        tool_settings = context.tool_settings

        if space_data:
            space_type = space_data.type
            if space_type == 'IMAGE_EDITOR':
                return 'PAINT_2D'
            elif space_type in {'VIEW_3D', 'PROPERTIES'}:
                if mode == 'PAINT_TEXTURE':
                    if tool_settings.image_paint:
                        return mode
                    else:
                        return None
                return mode
        return None    