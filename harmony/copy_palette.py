import bpy # type: ignore

class JOHNNYGIZMO_COLORHARMONY_OT_SavePaletteCopy(bpy.types.Operator):
    """Save a copy of the Harmony Palette as a new, standalone palette"""
    bl_idname = "johnnygizmo_colorharmony.save_palette_copy"
    bl_label = "Save a Copy of Palette"

    new_name: bpy.props.StringProperty(
        name="Palette Name",
        description="Name of the new palette",
        default="Harmony Palette Copy"
    ) # type: ignore

    def execute(self, context):
        src_palette = bpy.data.palettes.get("Harmony Palette")
        if not src_palette:
            self.report({'WARNING'}, "No Harmony Palette found to copy.")
            return {'CANCELLED'}

        # if self.new_name in bpy.data.palettes:
        #     self.report({'WARNING'}, f"Palette '{self.new_name}' already exists.")
        #     return {'CANCELLED'}

        new_palette = bpy.data.palettes.new(name=self.new_name)

        for color in src_palette.colors:
            new_color = new_palette.colors.new()
            new_color.color = color.color[:]

        self.report({'INFO'}, f"Palette '{self.new_name}' created with {len(new_palette.colors)} colors.")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(JOHNNYGIZMO_COLORHARMONY_OT_SavePaletteCopy)
def unregister():
    bpy.utils.unregister_class(JOHNNYGIZMO_COLORHARMONY_OT_SavePaletteCopy)