import bpy

class JOHNNYGIZMOCOLORHARMONY_OT_CopyToGlobalPalette(bpy.types.Operator):
    bl_idname = "johnnygizmo_colorharmony.copy_to_global_palette"
    bl_label = "Copy Harmony Palette to Global Palette"
    bl_description = "Copy generated harmony colors to a Blender global palette"

    palette_name: bpy.props.StringProperty(
        name="Palette Name",
        default="Harmony Palette"
    )

    overwrite_existing: bpy.props.BoolProperty(
        name="Overwrite Existing",
        description="Overwrite existing colors in the global palette",
        default=True
    )


    def execute(self, context):
        scene = context.scene
        colors = scene.johnnygizmo_harmony_palette  # your custom palette container

        # Try to find existing palette or create new one
        
        palette = bpy.data.palettes.get(self.palette_name)
        
        if self.overwrite_existing and palette:
            palette.colors.clear()
        else:
            palette = bpy.data.palettes.new(self.palette_name)

            for col in colors.colors:
                color = palette.colors.new()
                color.color = col.color[:3]


        self.report({'INFO'}, f"Copied {len(palette.colors)} colors to palette '{self.palette_name}'")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(JOHNNYGIZMOCOLORHARMONY_OT_CopyToGlobalPalette)

def unregister():
    bpy.utils.unregister_class(JOHNNYGIZMOCOLORHARMONY_OT_CopyToGlobalPalette)
