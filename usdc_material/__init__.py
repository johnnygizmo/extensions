# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
import zipfile
import tempfile
import os
import shutil
from bpy_extras.io_utils import ImportHelper


class IMPORT_OT_usdz_material(bpy.types.Operator, ImportHelper):
    """Import one or more AmbientCG USDZ material ZIP archives"""
    bl_idname = "import_scene.usdz_material"
    bl_label = "Import USDZ Materials"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".zip"
    filter_glob: bpy.props.StringProperty(default="*.zip", options={'HIDDEN'})
    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)

    def execute(self, context):
        directory = os.path.dirname(self.filepath)

        # Determine selected files
        if not self.files:
            zip_paths = [self.filepath]
        else:
            zip_paths = [os.path.join(directory, f.name) for f in self.files]

        for zip_path in zip_paths:
            self.report({'INFO'}, f"Importing {os.path.basename(zip_path)}")
            temp_dir = tempfile.mkdtemp()

            try:
                # 1. Unzip the archive
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                # 2. Find the .usdc file
                usdc_files = [f for f in os.listdir(temp_dir) if f.endswith('.usdc')]
                if not usdc_files:
                    self.report({'WARNING'}, f"No .usdc file found in {os.path.basename(zip_path)}")
                    continue

                usdc_path = os.path.join(temp_dir, usdc_files[0])
                print(f"Found USDZ file: {usdc_path}")

                existing_mats = set(bpy.data.materials.keys())

                # 3. Import the USD with materials
                bpy.ops.wm.usd_import(filepath=usdc_path, import_all_materials=True)

                # 4. Identify newly imported materials
                new_mats = [bpy.data.materials[name]
                            for name in bpy.data.materials.keys()
                            if name not in existing_mats]

                if not new_mats:
                    self.report({'WARNING'}, f"No new materials imported from {os.path.basename(zip_path)}")
                    continue

                new_mat = new_mats[0]

                # 5. Find Material Output node
                output_node = next((n for n in new_mat.node_tree.nodes if n.type == 'OUTPUT_MATERIAL'), None)

                # 6. Define grid layout for texture nodes
                if output_node:
                    grid_start_x = output_node.location.x + 400
                    grid_start_y = output_node.location.y
                else:
                    grid_start_x = 400
                    grid_start_y = 0
                node_spacing_x = 300
                node_spacing_y = 350
                nodes_per_row = 3

                # 7. Track existing images
                existing_images = {
                    node.image.name
                    for node in new_mat.node_tree.nodes
                    if node.type == 'TEX_IMAGE' and node.image
                }

                # 8. Add texture nodes for any missing images
                texture_nodes = []
                for img_file in os.listdir(temp_dir):
                    if img_file.lower().endswith(('.png', '.jpg', '.jpeg', '.tga', '.bmp', '.tiff')):
                        img_path = os.path.join(temp_dir, img_file)
                        img_name = os.path.splitext(img_file)[0]

                        # Avoid duplicates
                        if any(img_name.lower() in ex.lower() or ex.lower() in img_name.lower()
                               for ex in existing_images):
                            print(f"Skipping duplicate image: {img_file}")
                            continue

                        img = bpy.data.images.load(img_path)
                        tex_node = new_mat.node_tree.nodes.new('ShaderNodeTexImage')
                        tex_node.image = img
                        tex_node.label = img_file
                        texture_nodes.append(tex_node)
                        print(f"Added texture node: {img_file}")

                # 9. Position texture nodes in a grid
                for i, tex_node in enumerate(texture_nodes):
                    row = i // nodes_per_row
                    col = i % nodes_per_row
                    tex_node.location.x = grid_start_x + (col * node_spacing_x)
                    tex_node.location.y = grid_start_y - (row * node_spacing_y)

                # 10. Create a preview object
                new_mat.displacement_method = 'BOTH'
                bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=24)
                obj = context.active_object
                obj.name = f"ImportedSphere_{new_mat.name}"
                bpy.ops.object.shade_auto_smooth()

                # Assign material
                if not obj.data.materials:
                    obj.data.materials.append(new_mat)
                else:
                    obj.data.materials[0] = new_mat

                # 11. Tag as asset and adjust metadata
                new_mat.asset_mark()
                if new_mat.name.startswith("aCG_"):
                    new_mat.name = new_mat.name[4:]
                    new_mat.asset_data.author = "AmbientCG.com"
                    new_mat.asset_data.license = "Creative Commons CC0 1.0 Universal License"
                    print(f"Renamed material to: {new_mat.name}")

                # 12. Ensure UVMap node uses default name
                for node in new_mat.node_tree.nodes:
                    if node.type == 'UVMAP':
                        node.uv_map = "UVMap"

                new_mat.asset_generate_preview()
                bpy.ops.file.pack_all()

            except Exception as e:
                self.report({'ERROR'}, f"Failed importing {os.path.basename(zip_path)}: {e}")

            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)

        return {'FINISHED'}


def menu_func_import(self, context):
    self.layout.operator(IMPORT_OT_usdz_material.bl_idname, text="AmbientCG USD Materials (.zip)")


def register():
    bpy.utils.register_class(IMPORT_OT_usdz_material)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.utils.unregister_class(IMPORT_OT_usdz_material)


if __name__ == "__main__":
    register()
