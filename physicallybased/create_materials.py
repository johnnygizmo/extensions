import time
import bpy # type: ignore
import json
import urllib.request
import urllib.error

from . import materials  # Assuming materials.py is in the same directory


def create_material(mat, material_data):    
    if material_data.get("complexIor"): 
        materials.create_metallic_material(mat, material_data)
    else:
        materials.base_material_setup(mat, material_data)

class PHYSICALLYBASED_OT_create_materials(bpy.types.Operator):
    """Download materials from Physically Based API and create sphere objects"""
    bl_idname = "physicallybased.create_materials"
    bl_label = "Create Physically Based Materials"
    bl_options = {'REGISTER', 'UNDO'}
    
    api_url: bpy.props.StringProperty(
        name="API URL",
        # The line `default="https://api.physicallybased.info/materials"` in the `api_url` property
        # definition is setting a default value for the property.
        default="https://api.physicallybased.info/materials"
    )  # type: ignore
    
    def execute(self, context):
        # Download JSON data
        try:
            self.report({'INFO'}, f"Downloading materials from {self.api_url}...")
            with urllib.request.urlopen(self.api_url) as response:
                data = response.read()
                materials_data = json.loads(data)
        except urllib.error.URLError as e:
            self.report({'ERROR'}, f"Failed to download materials: {e}")
            return {'CANCELLED'}
        except json.JSONDecodeError as e:
            self.report({'ERROR'}, f"Failed to parse JSON: {e}")
            return {'CANCELLED'}
        
        if not isinstance(materials_data, list):
            self.report({'ERROR'}, "Expected JSON array")
            return {'CANCELLED'}
        
        # Track statistics
        created_count = 0
        
        # Create sphere objects with materials
        for i, material_data in enumerate(materials_data):
            material_name = material_data.get("name", f"Material_{i}")
            
            
            # Create sphere mesh
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=1.0,
                location=(i * 2.5, 0, 0)  # Offset each sphere
            )
            
            # Get the newly created object
            sphere_obj = context.active_object
            sphere_obj.name = material_name
            
            #set the sphere to smooth shading
            bpy.ops.object.shade_smooth()
            
            # Create material
            mat = bpy.data.materials.new(name=material_name)
            mat.use_nodes = True
            
            # Assign material to object
            if sphere_obj.data.materials:
                sphere_obj.data.materials[0] = mat
            else:
                sphere_obj.data.materials.append(mat)
            
            # Mark material as asset
            mat.asset_mark()
            
            # TODO: Configure material nodes based on material_data properties
            create_material(mat, material_data)
           
            
            
            # Generate asset preview from the sphere object
            mat.asset_data.author = "physicallybased.info"
            mat.asset_data.license = "Creative Commons CC0 1.0 Universal License"
            
            categories = material_data.get("category")
            for category in categories:
                mat.asset_data.tags.new(category)            
            
            
            taglist = material_data.get("tags", [])
            for tag in taglist:
                mat.asset_data.tags.new(tag)            
            
            
            
            created_count += 1
        
        self.report({'INFO'}, f"Created {created_count} sphere objects with materials")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(PHYSICALLYBASED_OT_create_materials)


def unregister():
    bpy.utils.unregister_class(PHYSICALLYBASED_OT_create_materials)
