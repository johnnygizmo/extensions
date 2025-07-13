bl_info = {
    "name": "Color Harmony Tools",
    "author": "Johnny",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "View3D > Sidebar > Color Tools",
    "description": "Generates color harmonies (complementary, split complementary) for materials.",
    "category": "Material",
}

import bpy # type: ignore
from . import harmony_colors
from . import ui_panel
from . import assign
from . import copy_palette


def register():
    harmony_colors.register()
    assign.register()
    ui_panel.register()
    copy_palette.register()

def unregister(): 
    ui_panel.unregister()
    assign.unregister()
    harmony_colors.unregister()
    copy_palette.unregister()
