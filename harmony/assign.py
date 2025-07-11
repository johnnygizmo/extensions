import bpy
from bpy.props import FloatVectorProperty, PointerProperty
from math import pow # Ensure pow is imported
from . import color_utils

class JOHNNYGIZMO_COLORHARMONY_OT_ApplySelectedPaletteColor(bpy.types.Operator):
    """Assign the active color of the 'Harmony Palette' to the active material's Base Color"""
    bl_idname = "colorharmony.apply_selected_palette_color"
    bl_label = "Apply Selected Palette Color"
    bl_options = {'REGISTER', 'UNDO'}

    destination: bpy.props.EnumProperty(
        name="Destination",
        description="Where to apply the selected palette color",
        items=[
            ('DIFFUSE', "Diffuse", "Apply to Diffuse Color"),
            ('SPECULAR', "Specular", "Apply to Specular Tint"),
            ('EMISSIVE', "Emissive", "Apply to Emissive Color"),
            ('COAT', "Coat", "Apply to Coat Tint"),
            ('SHEEN', "Sheen", "Apply to Sheen Tint"),
        ],
        default='DIFFUSE'
    )

    def execute(self, context):
        
        for obj in context.selected_objects:
            #obj = context.object
            
            if not obj:
                self.report({'WARNING'}, "No active object selected.")
                continue
                
            mat = obj.active_material
            
            if not mat:
                self.report({'WARNING'}, "Active object has no material.")
                continue

            if not mat.use_nodes:
                self.report({'WARNING'}, "Material does not use nodes.")
                continue
            
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if not bsdf:
                self.report({'WARNING'}, "Principled BSDF node not found in material.")
                continue

            palette = bpy.data.palettes.get("Harmony Palette")
            if not palette:
                self.report({'WARNING'}, "Harmony Palette not found. Please generate colors first.")
                continue

            # Get the active color from the palette
            # The 'active_color' is a reference to a bpy.types.PaletteColor object
            # and its 'color' property is a FloatVector (RGB) in linear space.
            if palette.colors.active:
                selected_color = palette.colors.active.color
                # Ensure it's a 4-element vector (RGBa) for the Base Color input
                # The alpha channel is usually 1.0 for Base Color unless specified otherwise.
                srgb_color = color_utils.convert_srgb_to_linear_rgb(selected_color[:3])
                
                if self.destination == 'DIFFUSE':
                    bsdf.inputs["Base Color"].default_value = (*srgb_color, 1.0)
                    mat.diffuse_color = (*srgb_color[:3], 1.0)
                elif self.destination == 'SPECULAR':
                    bsdf.inputs["Specular Tint"].default_value = (*srgb_color, 1.0)
                elif self.destination == 'EMISSIVE':
                    bsdf.inputs["Emission Color"].default_value = (*srgb_color, 1.0)
                elif self.destination == 'COAT':
                    bsdf.inputs["Coat Tint"].default_value = (*srgb_color, 1.0)
                elif self.destination == 'SHEEN':
                    bsdf.inputs["Sheen Tint"].default_value = (*srgb_color, 1.0)
                
            
            else:
                self.report({'WARNING'}, "No active color selected in the Harmony Palette.")
                return {'CANCELLED'}

        return {'FINISHED'}


class JOHNNYGIZMO_COLORHARMONY_OT_GetSelectedPaletteColor(bpy.types.Operator):
    """Get the active material's Base Color and set Base Color"""
    bl_idname = "johnnygizmo_colorharmony.get_base_palette_color"
    bl_label = "Get Base Palette Color"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        obj = context.object
        
        if not obj:
            self.report({'WARNING'}, "No active object selected.")
            return {'CANCELLED'}
            
        mat = obj.active_material
        
        if not mat:
            self.report({'WARNING'}, "Active object has no material.")
            return {'CANCELLED'}

        if not mat.use_nodes:
            self.report({'WARNING'}, "Material does not use nodes.")
            return {'CANCELLED'}
        
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if not bsdf:
            self.report({'WARNING'}, "Principled BSDF node not found in material.")
            return {'CANCELLED'}

        palette = bpy.data.palettes.get("Harmony Palette")
        if not palette:
            self.report({'WARNING'}, "Harmony Palette not found. Please generate colors first.")
            return {'CANCELLED'}

        # Get the active color from the palette
        # The 'active_color' is a reference to a bpy.types.PaletteColor object
        # and its 'color' property is a FloatVector (RGB) in linear space.

        if bsdf.inputs["Base Color"]:
            bpy.context.scene.johnnygizmo_harmony_base_color = bsdf.inputs["Base Color"].default_value  

        return {'FINISHED'}


def register():
    bpy.utils.register_class(JOHNNYGIZMO_COLORHARMONY_OT_ApplySelectedPaletteColor) # Register the new operator
    bpy.utils.register_class(JOHNNYGIZMO_COLORHARMONY_OT_GetSelectedPaletteColor)

def unregister():
    bpy.utils.unregister_class(JOHNNYGIZMO_COLORHARMONY_OT_ApplySelectedPaletteColor) # Unregister the new operator
    bpy.utils.unregister_class(JOHNNYGIZMO_COLORHARMONY_OT_GetSelectedPaletteColor)
