from multiprocessing import context
import bpy # type: ignore
from . import color_utils
from bpy.props import FloatVectorProperty, PointerProperty, IntProperty, FloatProperty, EnumProperty # type: ignore
from math import pi,ceil

class JOHNNYGIZMO_COLORHARMONY_OT_SetActivePaletteColor(bpy.types.Operator):
    """Set this color as the active color in the Harmony Palette"""
    bl_idname = "johnnygizmo_colorharmony.set_active_palette_color"
    bl_label = "Set Active Palette Color"
    index: bpy.props.IntProperty() # type: ignore

    def execute(self, context):
        palette = context.scene.johnnygizmo_harmony.palette
        color_s = color_utils.convert_srgb_to_linear_rgb(palette.colors[self.index].color)
        color = (
            "[ "
            + str(round(color_s[0],5))
            + ", "
            + str(round(color_s[1],5))
            + ", "
            + str(round(color_s[2],5))
            + ", 1.00000 ]"
        )
        bpy.context.window_manager.clipboard = color
        self.report({'INFO'}, color + " Copied to Clipboard.")
        if palette and 0 <= self.index < len(palette.colors):
            palette.colors.active = palette.colors[self.index]
        return {'FINISHED'}
