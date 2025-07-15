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
from . import harmony_settings
from . import save_palette_copy
from . import set_active_palette_color
from . import ui_material_panel
from . import ui_light_panel
from . import ui_palette_panel
from . import get_selected_node
from . import get_selected_palette_color
from . import palette_color_to_rgb_nodes
from . import apply_selected_palette_color


classes = (
    save_palette_copy.JOHNNYGIZMO_COLORHARMONY_OT_SavePaletteCopy,
    set_active_palette_color.JOHNNYGIZMO_COLORHARMONY_OT_SetActivePaletteColor,
    ui_light_panel.COLORHARMONY_PT_Light_Panel,
    ui_material_panel.COLORHARMONY_PT_material_panel,
    ui_palette_panel.COLORHARMONY_PT_palette_panel,
    get_selected_palette_color.JOHNNYGIZMO_COLORHARMONY_OT_GetSelectedPaletteColor,
    get_selected_node.JOHNNYGIZMO_COLORHARMONY_OT_GetSelectedNode,
    palette_color_to_rgb_nodes.JOHNNYGIZMO_COLORHARMONY_OT_PaletteColorToRGBNodes,
    apply_selected_palette_color.JOHNNYGIZMO_COLORHARMONY_OT_ApplySelectedPaletteColor           
)


def register():
    harmony_settings.register()

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister(): 
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    harmony_settings.unregister()




# classes = (
#     BulkAssetToolsPreferences,
#     ASSET_OT_MoveOperator,
#     ASSET_OT_AuthorOperator,
#     ASSET_OT_DescriptionOperator,
#     ASSET_OT_TagAddOperator,
#     ASSET_OT_TagCopyOperator,
#     ASSET_OT_TagRemoveOperator,
#     ASSET_OT_RenameOperator,
#     ASSET_OT_ClearOperator,
#     ASSET_OT_LicenseOperator,
#     ASSET_OT_CopyrightOperator
# )

# menus = (
#     ASSET_MT_move_menu_func,
#     ASSET_MT_author_menu_func,
#     ASSET_MT_license_menu_func,
#     ASSET_MT_copyright_menu_func,
#     ASSET_MT_description_menu_func,
#     ASSET_MT_tag_add_menu_func,
#     ASSET_MT_tag_copy_menu_func,
#     ASSET_MT_tag_remove_menu_func,
#     ASSET_MT_rename_menu_func,
#     ASSET_MT_clear_menu_func
# )

# def register():
#     for cls in classes:
#         bpy.utils.register_class(cls)
        
#     bpy.types.ASSETBROWSER_MT_context_menu.append(header_menu_func)
#     if hasattr(bpy.types,"ASSETBROWSER_MT_asset"):
#         bpy.types.ASSETBROWSER_MT_asset.append(header_menu_func)
#     elif hasattr(bpy.types,"ASSETBROWSER_MT_edit"):
#         bpy.types.ASSETBROWSER_MT_edit.append(header_menu_func)
        

#     for menu in menus:
#         if hasattr(bpy.types,"ASSETBROWSER_MT_asset"):
#             bpy.types.ASSETBROWSER_MT_asset.append(menu)
#         elif hasattr(bpy.types,"ASSETBROWSER_MT_edit"):
#             bpy.types.ASSETBROWSER_MT_edit.append(menu)
#         bpy.types.ASSETBROWSER_MT_context_menu.append(menu)


# def unregister():
#     bpy.types.ASSETBROWSER_MT_context_menu.remove(header_menu_func)

#     if hasattr(bpy.types,"ASSETBROWSER_MT_asset"):
#         bpy.types.ASSETBROWSER_MT_asset.remove(header_menu_func)
#     elif hasattr(bpy.types,"ASSETBROWSER_MT_edit"):
#         bpy.types.ASSETBROWSER_MT_edit.remove(header_menu_func)

#     for menu in menus:
#         if hasattr(bpy.types,"ASSETBROWSER_MT_asset"):
#             bpy.types.ASSETBROWSER_MT_asset.remove(menu)
#         elif hasattr(bpy.types,"ASSETBROWSER_MT_edit"):
#             bpy.types.ASSETBROWSER_MT_edit.remove(menu)
#         bpy.types.ASSETBROWSER_MT_context_menu.remove(menu)

#     for cls in reversed(classes):
#         bpy.utils.unregister_class(cls)

# if __name__ == "__main__":
#     register()
