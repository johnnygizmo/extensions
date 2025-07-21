import bpy

def panelHead(layout, node):
    panel_header, panel_layout  = layout.panel(f"Modifier Node: {node.name}", default_closed=True)
    title = node.name
    if(node.label != ""):
        title = node.label + " (" + node.name + ")"

    row = panel_header.row()
    row.alignment = 'LEFT'
    row.label(text =  title)

    if panel_layout is None:
        return None 

    return panel_layout


def modifier_font_menu(self, context):
    layout = self.layout
    obj = context.object
    if not obj:
        return None
    active_mod = next((m for m in obj.modifiers if getattr(m, "is_active", False)), None)
    if not active_mod or active_mod.type != 'NODES':
        return None
    if not hasattr(active_mod, "node_group") or not active_mod.node_group:
        return None
    gn_mod = next((m for m in obj.modifiers if m.type == 'NODES'), None)
    scene = context.scene
    node_count = 0
    if gn_mod:
        for b in gn_mod.bakes:
            
            if b.node:
                if not b.node.hide and not b.node.mute: 
                    node_count += 1                   
                    if (box := panelHead(layout, b.node)) is None:
                        continue
                    row = box.row()
                
                    op = row.operator("object.johnnygizmo_geometry_node_bake", text="Bake", icon='NONE')
                    op.action = 1
                    op.session_uid = obj.session_uid
                    op.modifier_name = gn_mod.name
                    op.bake_id = b.bake_id
             
                    op2 = row.operator("object.johnnygizmo_geometry_node_bake", text="", icon='TRASH')
                    op2.action = 0                   
                    op2.session_uid = obj.session_uid
                    op2.modifier_name = gn_mod.name
                    op2.bake_id = b.bake_id   

        for n in gn_mod.node_group.nodes: 
            #print(n.bl_idname, n.hide, n.mute)
            if n.bl_idname == "GeometryNodeStringToCurves" and n.hide == False and n.mute == False:
                node_count += 1 
                if (box := panelHead(layout, n)) is None:
                    continue

                row = box.row()
                row.template_ID(n, "font", open="font.open", unlink="font.unlink") 
                row = box.row()
                row.label(text="Overflow:")
                row.prop(n, "overflow", text="")
                row = box.row()
                row.prop(n, "align_x", text="Horizontal")
                row = box.row()
                row.prop(n, "align_y", text="Vertical")
                row = box.row()
                row.prop(n, "pivot_mode", text="Pivot Point")
                row = layout.row()
            elif n.bl_idname == "ShaderNodeFloatCurve" and n.hide == False and n.mute == False:
                node_count += 1 
                if (box := panelHead(layout, n)) is None:
                    continue
                row = box.row()
                box.template_curve_mapping(n, "mapping")

            elif n.bl_idname == "ShaderNodeVectorCurve" and n.hide == False and n.mute == False:
                node_count += 1 
                if (box := panelHead(layout, n)) is None:
                    continue
                row = box.row()
                box.template_curve_mapping(n, "mapping",type='VECTOR')       
            elif n.bl_idname ==  n.bl_idname == "ShaderNodeRGBCurve" and n.hide == False and n.mute == False:
                node_count += 1 
                if (box := panelHead(layout, n)) is None:
                    continue
                row = box.row()
                box.template_curve_mapping(n, "mapping",type='COLOR')                                                       
            elif n.bl_idname ==  n.bl_idname == "ShaderNodeValToRGB" and n.hide == False and n.mute == False:
                node_count += 1 
                if (box := panelHead(layout, n)) is None:
                    continue
                row = box.row()
                box.template_color_ramp(n, "color_ramp",expand=True)     

            elif n.bl_idname ==  n.bl_idname == "ShaderNodeTexBrick" and n.hide == False and n.mute == False:
                node_count += 1 
                if (box := panelHead(layout, n)) is None:
                    continue
                row = box.row()                
                row.prop(n, "offset", text="Offset")
                row = box.row()                
                row.prop(n, "offset_frequency", text="Frequency")
                row = box.row()                
                row.prop(n, "squash", text="Squash")
                row = box.row()                
                row.prop(n, "squash_frequency", text="Squash Frequency")
            elif n.bl_idname ==  n.bl_idname == "GeometryNodeImageTexture" and n.hide == False and n.mute == False:
                node_count += 1 
                if (box := panelHead(layout, n)) is None:
                    continue
                row = box.row()                
                row.prop(n, "interpolation", text="Interpolation")
                row = box.row()                
                row.prop(n, "extension", text="Extension")
            elif n.bl_idname ==  n.bl_idname == "ShaderNodeTexMagic" and n.hide == False and n.mute == False:
                node_count += 1 
                if (box := panelHead(layout, n)) is None:
                    continue
                row = box.row()                
                row.prop(n, "turbulence_depth", text="Depth")      
            elif n.bl_idname ==  n.bl_idname == "ShaderNodeTexNoise" and n.hide == False and n.mute == False:
                node_count += 1 
                if (box := panelHead(layout, n)) is None:
                    continue
                row = box.row()                
                row.prop(n, "noise_type", text="Type")       
                row = box.row()                
                row.prop(n, "noise_dimensions", text="Dimensions")      
                row = box.row()       
                row.label(text="Will cause socket changes", icon='ERROR' ) 
            elif n.bl_idname ==  n.bl_idname == "ShaderNodeTexVoronoi" and n.hide == False and n.mute == False:
                node_count += 1 
                if (box := panelHead(layout, n)) is None:
                    continue
                row = box.row()                
                row.prop(n, "voronoi_dimensions", text="Dimensions") 
                row = box.row()                
                row.prop(n, "feature", text="Feature")
                row = box.row()                
                row.prop(n, "distance", text="Distance")
                row = box.row()                
                row.prop(n, "normalize", text="Normalize")         
                row = box.row()       
                row.label(text="Will cause socket changes", icon='ERROR' )        
            elif n.bl_idname ==  n.bl_idname == "ShaderNodeTexWave" and n.hide == False and n.mute == False:
                node_count += 1 
                if (box := panelHead(layout, n)) is None:
                    continue
                row = box.row()                
                row.prop(n, "wave_type", text="Type") 
                row = box.row()
                if n.wave_type == 'RINGS':
                    row.prop(n, "rings_direction", text="Direction")
                else:
                    row.prop(n, "bands_direction", text="Direction")                
                row = box.row()
                row.prop(n, "wave_profile", text="Profile")
            elif n.bl_idname ==  n.bl_idname == "ShaderNodeTexWhiteNoise" and n.hide == False and n.mute == False:
                node_count += 1 
                if (box := panelHead(layout, n)) is None:
                    continue
                row = box.row()                
                row.prop(n, "noise_dimensions", text="Dimensions") 
            elif n.bl_idname ==  n.bl_idname == "ShaderNodeTexGabor" and n.hide == False and n.mute == False:
                node_count += 1 
                if (box := panelHead(layout, n)) is None:
                    continue            
                row = box.row()                
                row.prop(n, "gabor_type", text="Type")                           
                row = box.row()       
                row.label(text="Will cause socket changes", icon='ERROR' ) 
            elif n.bl_idname ==  n.bl_idname == "ShaderNodeTexGradient" and n.hide == False and n.mute == False:
                node_count += 1 
                if (box := panelHead(layout, n)) is None:
                    continue            
                row = box.row()                
                row.prop(n, "gradient_type", text="Type")   
            elif n.bl_idname ==  n.bl_idname == "FunctionNodeCombineColor" and n.hide == False and n.mute == False:
                node_count += 1 
                if (box := panelHead(layout, n)) is None:
                    continue            
                row = box.row()                
                row.prop(n, "mode", text="Mode") 
            elif n.bl_idname ==  n.bl_idname == "ShaderNodeMix" and n.hide == False and n.mute == False:
                node_count += 1 
                if (box := panelHead(layout, n)) is None:
                    continue            
                row = box.row()                
                row.prop(n, "data_type", text="Data Type")
                if n.data_type == 'FLOAT':
                    row = box.row()                
                    row.prop(n, "clamp_factor", text="Clamp Factor")
                if n.data_type == 'VECTOR':                    
                    row = box.row()                
                    row.prop(n, "factor_mode", text="Factor Mode")
                    row = box.row()                
                    row.prop(n, "clamp_factor", text="Clamp Factor")
                if n.data_type == 'RGBA':
                    row = box.row()                
                    row.prop(n, "blend_type", text="Blend Type")
                    row = box.row()                
                    row.prop(n, "clamp_result", text="Clamp Result")
                    row = box.row()                
                    row.prop(n, "clamp_factor", text="Clamp Factor")
                if n.data_type == 'ROTATION':                    
                    row = box.row()                
                    row.prop(n, "clamp_factor", text="Clamp Factor")
                row = box.row()       
                row.label(text="Will cause socket changes", icon='ERROR' )   






        if gn_mod.node_group.users > 1 and node_count > 0:
            row = layout.row()
            row.label(text=f"{gn_mod.node_group.users} modifier uses will be updated", icon='MODIFIER')
        row = layout.row()
        row.separator()
        
    else:
        layout.label(text="No Geometry Nodes modifier found.")            


def register():
    bpy.types.DATA_PT_modifiers.append(modifier_font_menu)

def unregister():
    bpy.types.DATA_PT_modifiers.remove(modifier_font_menu)