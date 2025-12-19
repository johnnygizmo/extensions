import bpy
import os
import shutil
import json
from bpy.props import StringProperty
from bpy.types import Operator

class ICONPACK_OT_export_icons(Operator):
    """Export Blender internal SVG icons to a format compatible with Stream Deck"""
    bl_idname = "iconpack.export_icons"
    bl_label = "Export Blender Icons (SVG)"
    bl_options = {'REGISTER', 'UNDO'}

    directory: StringProperty(
        name="Export Directory",
        description="Directory to export icons to",
        subtype='DIR_PATH'
    )

    def execute(self, context):
        if not self.directory:
            self.report({'ERROR'}, "Please select a directory")
            return {'CANCELLED'}

        # Prepare directory structure
        base_dir = self.directory
        icons_dir = os.path.join(base_dir, "Icons")
        
        try:
            os.makedirs(icons_dir, exist_ok=True)
        except OSError as e:
            self.report({'ERROR'}, f"Failed to create directory: {e}")
            return {'CANCELLED'}

        # Find SVG Icons
        # Typical path: [Blender Path]/[Version]/datafiles/icons_svg
        # We can use bpy.utils.resource_path('DATAFILES') to get the datafiles root.
        
        datafiles_path = bpy.utils.resource_path('DATAFILES')
        svg_icons_path = os.path.join(datafiles_path, "icons_svg")
        
        if not os.path.exists(svg_icons_path):
             # Fallback check for standard install structure if resource_path returns something unexpected
             # Sometimes resource_path('DATAFILES') points deeper or shallower depending on env
             # Let's try to search relative to binary if above fails, but that's platform specific.
             # For now, report error if generic path fails.
             self.report({'ERROR'}, f"SVG icons not found at: {svg_icons_path}")
             return {'CANCELLED'}

        # Export Icons
        exported_count = 0
        error_count = 0
        
        svg_files = [f for f in os.listdir(svg_icons_path) if f.lower().endswith(".svg")]
        
        if not svg_files:
            self.report({'WARNING'}, f"No SVG files found in {svg_icons_path}")
            return {'CANCELLED'}

        for icon_file in svg_files:
            try:
                src_path = os.path.join(svg_icons_path, icon_file)
                dst_path = os.path.join(icons_dir, icon_file)
                shutil.copy2(src_path, dst_path)
                exported_count += 1
            except Exception as e:
                print(f"Failed to copy {icon_file}: {e}")
                error_count += 1

        # Create Info File
        info = {
            "Name": "Blender SVG Icons",
            "Version": "1.0.0",
            "Description": f"Collection of {exported_count} scalable Blender icons.",
            "Author": "Blender Foundation / Extension",
            "URL": "https://blender.org",
            "Icon": "blender.svg" if "blender.svg" in svg_files else (svg_files[0] if svg_files else ""),
            "License": "GPL-3.0"
        }
        
        with open(os.path.join(base_dir, "icon_pack.json"), 'w') as f:
            json.dump(info, f, indent=4)

        self.report({'INFO'}, f"Exported {exported_count} SVG icons to {icons_dir}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
