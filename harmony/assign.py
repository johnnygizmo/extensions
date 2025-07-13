import bpy # type: ignore
from bpy.props import FloatVectorProperty, PointerProperty # type: ignore
from math import pow # Ensure pow is imported
from . import color_utils
from . import harmony_colors


def setNode(mat, props):
    if mat.node_tree.nodes.get(props.target_bsdf_node_name) is None:
        props.target_bsdf_node_name = ""
    elif mat.node_tree.nodes.get(props.target_bsdf_node_name).type not in harmony_colors.type_list:
        props.target_bsdf_node_name = ""

    if not props.target_bsdf_node_name:            
        for node in mat.node_tree.nodes:
            if node.type in harmony_colors.type_list:
                props.target_bsdf_node_name = node.name
                break


class JOHNNYGIZMO_COLORHARMONY_OT_ApplySelectedPaletteColor(bpy.types.Operator):
    """Assign the active color of the 'Harmony Palette' to the active material's Base Color"""
    bl_idname = "johnnygizmo_colorharmony.apply_selected_palette_color"
    bl_label = "Apply Selected Palette Color"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    
    input: bpy.props.StringProperty(
        name="Input",
        description="Input name to apply the color to",
        default="Base Color"
    ) # type: ignore

    def execute(self, context):
        props = context.scene.johnnygizmo_harmony
        for obj in context.selected_objects:            
            if not obj:
                self.report({'WARNING'}, "No active object selected.")
                continue
                
            mat = obj.active_material
            
            if not mat:
                self.report({'WARNING'}, obj.name+ " has no active material.")
                continue

            if not mat.use_nodes:
                self.report({'WARNING'}, "Material on " + obj.name+ " does not use nodes.")
                continue
            bsdf = mat.node_tree.nodes.get(props.target_bsdf_node_name)
            
            if not bsdf:
                self.report({'WARNING'}, "Node "+props.target_bsdf_node_name+ " not found in material on " + obj.name)
                continue

            palette = bpy.data.palettes.get("Harmony Palette")
            if not palette:
                self.report({'WARNING'}, "Harmony Palette not found. Please generate colors first.")
                continue
            if palette.colors.active:
                selected_color = palette.colors.active.color
                srgb_color = color_utils.convert_srgb_to_linear_rgb(selected_color[:3])
                
                if self.input == "CREATERGBNODE":
                    nodes = mat.node_tree.nodes
                    rgb_node = nodes.new(type='ShaderNodeRGB')
                    new_name = (
                        props.mode
                        + " [ "
                        + str(round(props.base_color[0],3)) + ", "
                        + str(round(props.base_color[1],3)) + ", "
                        + str(round(props.base_color[2],3))
                        + " ]"
                    )

                    rgb_node.label = new_name
                    rgb_node.name = "Harmony"  # This sets the actual ID name
                    rgb_node.location = (200, 200)
                    rgb_node.outputs[0].default_value = (*selected_color[:3], 1.0)  # RGBA
                elif self.input == "CREATERGBNODES":
                    nodes = mat.node_tree.nodes
                    
                    for idx in range(0,len(palette.colors)):
                        rgb_node = nodes.new(type='ShaderNodeRGB')
                        
                        new_name = (
                            props.mode
                            + " [ "
                            + str(round(props.base_color[0],3)) + ", "
                            + str(round(props.base_color[1],3)) + ", "
                            + str(round(props.base_color[2],3))
                            + " ] : " + str(idx)
                        )
                        
                        
                        
                        rgb_node.label = new_name
                        rgb_node.name = "Harmony"  # This sets the actual ID name
                        rgb_node.location = ( idx*75, -idx*50)
                        srgb_color = color_utils.convert_srgb_to_linear_rgb(palette.colors[idx].color[:3])
                        rgb_node.outputs[0].default_value = (*srgb_color[:3], 1.0)                     
                else:

                    if(self.input == "Color" or self.input == "Base Color"):
                        mat.diffuse_color = (*srgb_color[:3], 1.0)

                    bsdf.inputs[self.input].default_value = (*srgb_color, 1.0)            
            else:
                self.report({'WARNING'}, "No active color selected in the Harmony Palette.")
                return {'CANCELLED'}

        return {'FINISHED'}


class JOHNNYGIZMO_COLORHARMONY_OT_GetSelectedPaletteColor(bpy.types.Operator):
    """Get the active material's Base Color and set Base Color"""
    bl_idname = "johnnygizmo_colorharmony.get_base_palette_color"
    bl_label = "Get Base Palette Color"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        props = context.scene.johnnygizmo_harmony
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
               
        setNode(mat, props)

        if mat.node_tree.nodes.get(props.target_bsdf_node_name) is None:
           props.target_bsdf_node_name = ""
        elif mat.node_tree.nodes.get(props.target_bsdf_node_name).type not in harmony_colors.type_list:
           props.target_bsdf_node_name = ""

        if not props.target_bsdf_node_name:            
            for node in mat.node_tree.nodes:
                if node.type in harmony_colors.type_list:
                    props.target_bsdf_node_name = node.name
                    break

        bsdf = mat.node_tree.nodes.get(props.target_bsdf_node_name)

        if not bsdf:
            self.report({'WARNING'}, "Selected node not found in material.")
            return {'CANCELLED'}

        palette = bpy.data.palettes.get("Harmony Palette")
        if not palette:
            self.report({'WARNING'}, "Harmony Palette not found. Please generate colors first.")
            return {'CANCELLED'}
        
        if bsdf.inputs.get("Base Color") is not None:
            props.base_color = bsdf.inputs["Base Color"].default_value
        elif bsdf.inputs.get("Color") is not None:
            props.base_color = bsdf.inputs["Color"].default_value

        return {'FINISHED'}

class JOHNNYGIZMO_COLORHARMONY_OT_GetSelectedNode(bpy.types.Operator):
    """Get the active Node BSDF"""
    bl_idname = "johnnygizmo_colorharmony.get_node"
    bl_label = "Get Node"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def execute(self, context):
        props = context.scene.johnnygizmo_harmony
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
               
        setNode(mat, props)

        # if mat.node_tree.nodes.get(props.target_bsdf_node_name) is None:
        #    props.target_bsdf_node_name = ""
        # elif mat.node_tree.nodes.get(props.target_bsdf_node_name).type not in harmony_colors.type_list:
        #    props.target_bsdf_node_name = ""

        # if not props.target_bsdf_node_name:            
        #     for node in mat.node_tree.nodes:
        #         if node.type in harmony_colors.type_list:
        #             props.target_bsdf_node_name = node.name
        #             break

        # bsdf = mat.node_tree.nodes.get(props.target_bsdf_node_name)

        # if not bsdf:
        #     self.report({'WARNING'}, "Selected node not found in material.")
        #     return {'CANCELLED'}

        # palette = bpy.data.palettes.get("Harmony Palette")
        # if not palette:
        #     self.report({'WARNING'}, "Harmony Palette not found. Please generate colors first.")
        #     return {'CANCELLED'}
        
        # if bsdf.inputs.get("Base Color") is not None:
        #     props.base_color = bsdf.inputs["Base Color"].default_value
        # elif bsdf.inputs.get("Color") is not None:
        #     props.base_color = bsdf.inputs["Color"].default_value
        return {'FINISHED'}




def register():
    bpy.utils.register_class(JOHNNYGIZMO_COLORHARMONY_OT_ApplySelectedPaletteColor) 
    bpy.utils.register_class(JOHNNYGIZMO_COLORHARMONY_OT_GetSelectedPaletteColor)
    bpy.utils.register_class(JOHNNYGIZMO_COLORHARMONY_OT_GetSelectedNode)


def unregister():
    bpy.utils.unregister_class(JOHNNYGIZMO_COLORHARMONY_OT_ApplySelectedPaletteColor) 
    bpy.utils.unregister_class(JOHNNYGIZMO_COLORHARMONY_OT_GetSelectedPaletteColor)
    bpy.utils.unregister_class(JOHNNYGIZMO_COLORHARMONY_OT_GetSelectedNode)
