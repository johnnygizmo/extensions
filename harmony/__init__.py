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
from . import ui_material_panel
from . import assign
from . import copy_palette
from . import ui_light_panel


def register():
    harmony_colors.register()
    assign.register()
    copy_palette.register()
    ui_light_panel.register()
    ui_material_panel.register()

def unregister(): 
    ui_light_panel.unregister()
    ui_material_panel.unregister()
    copy_palette.unregister()
    assign.unregister()
    harmony_colors.unregister()
