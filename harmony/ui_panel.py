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

        layout.operator("johnnygizmo_colorharmony.get_base_palette_color",text="Get Diffuse")
        
        layout.prop(scene, "johnnygizmo_harmony_base_color", text="")
        layout.prop(colors, "harmony_mode", text="Type")
        if colors.harmony_mode in {'analogous'}:
            row = layout.row()
            row.prop(scene, "johnnygizmo_harmony_count", text="Colors")
            row.prop(scene, "johnnygizmo_analogous_angle", text="Angle")
            if scene.johnnygizmo_harmony_count % 2 == 0:
                layout.label(text="Count must be odd, adding 1 to make it "+ str(scene.johnnygizmo_harmony_count + 1))

        if colors.harmony_mode in {'monochromatic'}:
            layout.prop(scene, "johnnygizmo_harmony_count", text="Generated Steps")

        if colors.harmony_mode == 'tetradic':
            layout.prop(scene, "johnnygizmo_tetradic_angle", text="Tetradic Angle")

        # Display the palette assigned to this scene
        palette = scene.johnnygizmo_harmony_palette
        row = layout.row()
        row.scale_y = 1
        column = row.column(align=True)
        if palette:
            column.template_palette(scene,"johnnygizmo_harmony_palette", color=False)
        else:
            column.label(text="No palette assigned.")
        

        row = layout.row(align=True)
        op = row.operator("colorharmony.apply_selected_palette_color", text="Set Diffuse").destination = 'DIFFUSE'
        row.operator("colorharmony.apply_selected_palette_color", text="Specular").destination = 'SPECULAR'
        row = layout.row(align=True)
        row.operator("colorharmony.apply_selected_palette_color", text="Emissive").destination = 'EMISSIVE'
        row.operator("colorharmony.apply_selected_palette_color", text="Coat").destination = 'COAT'
        row.operator("colorharmony.apply_selected_palette_color", text="Sheen").destination = 'SHEEN'

def register():
    bpy.utils.register_class(COLORHARMONY_PT_Panel)
    # bpy.utils.register_class(COLORHARMONY_OT_GenerateColors)
    
def unregister():
    bpy.utils.unregister_class(COLORHARMONY_PT_Panel)
    # bpy.utils.unregister_class(COLORHARMONY_OT_GenerateColors)