bl_info = {
    "name": "Color Harmony Tools",
    "author": "Johnny",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "View3D > Sidebar > Color Tools",
    "description": "Generates color harmonies (complementary, split complementary) for materials.",
    "category": "Material",
}

import bpy
from . import harmony_colors
from . import ui_panel, color_utils
from . import copy_to_global


def register():
    harmony_colors.register()
    color_utils.register()
    copy_to_global.register()
    ui_panel.register()

def unregister():
    ui_panel.unregister()
    color_utils.unregister()
    harmony_colors.unregister()
    copy_to_global.unregister()
