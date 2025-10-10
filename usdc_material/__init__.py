# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
import zipfile
import tempfile
import os
from bpy_extras.io_utils import ImportHelper

class IMPORT_OT_usdz_material(bpy.types.Operator, ImportHelper):
    bl_idname = "import_scene.usdz_material"
    bl_label = "Import USDZ Material"
    bl_options = {'REGISTER', 'UNDO'}
    filename_ext = ".zip"
    filter_glob: bpy.props.StringProperty(default="*.zip", options={'HIDDEN'})

    def execute(self, context):
        temp_dir = tempfile.mkdtemp()
        zip_path = self.filepath

        # 1. Unzip the archive
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # 2. Find the .usdc file
        usdc_files = [f for f in os.listdir(temp_dir) if f.endswith('.usdc')]
        if not usdc_files:
            self.report({'ERROR'}, "No .usdc file found in zip")
            return {'CANCELLED'}
        else:
            print(f"Extracted files: {usdc_files}")

        usdc_path = os.path.join(temp_dir, usdc_files[0])
        print(f"Found USDZ file: {usdc_path}")
        existing_mats = set(bpy.data.materials.keys())

        # 4. Import the USD with materials
        bpy.ops.wm.usd_import(filepath=usdc_path, import_all_materials=True)

        # 5. Find newly created materials
        new_mats = [bpy.data.materials[name] for name in bpy.data.materials.keys() if name not in existing_mats]

        if not new_mats:
            self.report({'WARNING'}, "No new materials were imported.")
            return {'CANCELLED'}

        # Use the first new material found (or modify logic if multiple)
        new_mat = new_mats[0]
        
        # Find the output node to position texture nodes relative to it
        output_node = None
        for node in new_mat.node_tree.nodes:
            if node.type == 'OUTPUT_MATERIAL':
                output_node = node
                break
        
        # Set grid parameters for texture node layout
        if output_node:
            grid_start_x = output_node.location.x + 400  # Start grid 400 units to the right of output
            grid_start_y = output_node.location.y
            node_spacing_x = 300  # Horizontal spacing between nodes
            node_spacing_y = 350  # Vertical spacing between nodes
            nodes_per_row = 3     # Number of nodes per row in the grid
        else:
            # Fallback positions if no output node found
            grid_start_x = 400
            grid_start_y = 0
            node_spacing_x = 300
            node_spacing_y = 350
            nodes_per_row = 3
        
        # Get list of images already used in the material tree
        existing_images = set()
        for node in new_mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE' and node.image:
                existing_images.add(node.image.name)
        
        # for each image in the temp folder, add a texture node to the material only if not already present
        texture_nodes = []
        for img_file in os.listdir(temp_dir):
            if img_file.lower().endswith(('.png', '.jpg', '.jpeg', '.tga', '.bmp', '.tiff')):
                img_path = os.path.join(temp_dir, img_file)
                
                # Check if this image is already loaded in Blender and used in the material
                img_name = os.path.splitext(img_file)[0]  # Get filename without extension
                image_already_exists = False
                
                # Check if image with this name (or similar) already exists in the material
                for existing_img_name in existing_images:
                    if img_name.lower() in existing_img_name.lower() or existing_img_name.lower() in img_name.lower():
                        image_already_exists = True
                        print(f"Skipping {img_file} - similar image '{existing_img_name}' already exists in material")
                        break
                
                if not image_already_exists:
                    img = bpy.data.images.load(img_path)
                    tex_node = new_mat.node_tree.nodes.new('ShaderNodeTexImage')
                    tex_node.image = img
                    tex_node.label = img_file
                    texture_nodes.append(tex_node)
                    print(f"Added texture node for image: {img_file}")
                else:
                    print(f"Image {img_file} already exists in material tree, skipping")
        
        # Position texture nodes in a grid layout
        for i, tex_node in enumerate(texture_nodes):
            row = i // nodes_per_row
            col = i % nodes_per_row
            tex_node.location.x = grid_start_x + (col * node_spacing_x)
            tex_node.location.y = grid_start_y - (row * node_spacing_y)
        
        print(f"Imported new material: {new_mat.name}")
        print(f"Imported material: {new_mat.name if new_mat else 'None'}")
        # 5. Create an object and assign the material
        if new_mat:

            
            bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=24)
            obj = context.active_object
            obj.name = "ImportedSphere"
            bpy.ops.object.shade_auto_smooth()


            # Assign the material
            if len(obj.data.materials) == 0:
                obj.data.materials.append(new_mat)
            else:
                obj.data.materials[0] = new_mat

            # 6. Mark material as an asset
            new_mat.asset_mark()
            if new_mat.name.startswith("aCG_"):
                print("Material name starts with 'aCG_'")
                new_mat.name = new_mat.name[4:]
                new_mat.asset_data.author = "AmbientCG.com"
                new_mat.asset_data.license = "Creative Commons CC0 1.0 Universal License"
                print(f"Renamed material to: {new_mat.name}")
            # 7. Rename UVMap node if present
            for node in new_mat.node_tree.nodes:
                if node.type == 'UVMAP':
                    node.uv_map = "UVMap"
            
            new_mat.asset_generate_preview()

            bpy.ops.file.pack_all()

        return {'FINISHED'}

def menu_func_import(self, context):
    self.layout.operator(IMPORT_OT_usdz_material.bl_idname, text="AmbientCG USD Material (.zip)")

def register():
    bpy.utils.register_class(IMPORT_OT_usdz_material)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.utils.unregister_class(IMPORT_OT_usdz_material)
