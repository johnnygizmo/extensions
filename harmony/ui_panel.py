import bpy
from . import color_utils

class COLORHARMONY_PT_Panel(bpy.types.Panel):
    bl_label = "Color Harmony Tools"
    bl_idname = "COLORHARMONY_PT_material_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        colors = scene.johnnygizmo_harmony_colors

        layout.prop(colors, "harmony_mode", text="Type")
        layout.prop(scene, "johnnygizmo_harmony_base_color", text="")
        
        #only show Number of Outputs if monochromatic or analogous
        if colors.harmony_mode in {'analogous', 'monochromatic'}:
            layout.prop(scene, "johnnygizmo_harmony_count", text="Number of Outputs")

        if colors.harmony_mode == 'tetradic':
            layout.prop(scene, "johnnygizmo_tetradic_angle", text="Tetradic Angle")

        # Display the palette assigned to this scene
        palette = scene.johnnygizmo_harmony_palette
        row = layout.row()
        row.scale_y = 2
        column = row.column(align=True)
        if palette:
            column.template_palette(scene,"johnnygizmo_harmony_palette", color=False)
        else:
            column.label(text="No palette assigned.")
        
        row.operator("johnnygizmo_colorharmony.copy_to_global_palette", text="Save New")

        op = row.operator("johnnygizmo_colorharmony.copy_to_global_palette", text="Save")
        op.overwrite_existing = True


class COLORHARMONY_OT_GenerateColors(bpy.types.Operator):
    bl_idname = "colorharmony.generate_colors"
    bl_label = "Generate Color Harmonies"
    bl_description = "Generate harmony colors based on the base color"

    def execute(self, context):
        scene = context.scene
        colors = scene.johnnygizmo_harmony_colors
        base = scene.johnnygizmo_harmony_base_color

        colors.comp = color_utils.get_complementary_color(base)
        colors.split1, colors.split2 = color_utils.get_split_complementary_colors(base)

        self.report({'INFO'}, "Colors generated.")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(COLORHARMONY_PT_Panel)
    bpy.utils.register_class(COLORHARMONY_OT_GenerateColors)
    
def unregister():
    bpy.utils.unregister_class(COLORHARMONY_PT_Panel)
    bpy.utils.unregister_class(COLORHARMONY_OT_GenerateColors)