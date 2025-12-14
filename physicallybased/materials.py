def common_setup(mat, material_data):
    if material_data.get("color"):
        base_color = material_data["color"]
        if len(base_color) == 3:
            base_color.append(1.0)
        mat.diffuse_color = base_color
        
    if material_data.get("metalness"):
        mat.metallic = material_data.get("metalness")

    if material_data.get("roughness") is not None:
        mat.roughness = material_data.get("roughness")

def base_material_setup(mat,material_data):
    # Basic material setup code here
    # create node tree, add Principled BSDF, set base color, roughness, metallic, etc.
    if material_data.get("color"):
        base_color = material_data["color"]
        #convert to RGBA if necessary
        if len(base_color) == 3:  # If RGB, add alpha
            base_color.append(1.0)
        mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = base_color
    
    
    if material_data.get("specularColor") is not None:
        specular_color = material_data["specularColor"]
        if len(specular_color) == 3:
            specular_color.append(1.0)
        mat.node_tree.nodes["Principled BSDF"].inputs["Specular"].default_value = max(specular_color[0], specular_color[1], specular_color[2])
    
    if material_data.get("roughness") is not None:
        roughness = material_data["roughness"]
        mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = roughness

    if material_data.get("metallic") is not None:
        metallic = material_data["metallic"]
        mat.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = metallic
    
    if material_data.get("ior") is not None:
        ior = material_data["ior"]
        mat.node_tree.nodes["Principled BSDF"].inputs["IOR"].default_value = ior
    
    if material_data.get("transmission") is not None:
        transmission = material_data["transmission"]
        mat.node_tree.nodes["Principled BSDF"].inputs["Transmission Weight"].default_value = transmission
    
    if material_data.get("subsurfaceRadius"):
        subsurface_radius = material_data["subsurfaceRadius"]
        
        mat.node_tree.nodes["Principled BSDF"].inputs["Subsurface Weight"].default_value = 1
        
        mat.node_tree.nodes["Principled BSDF"].inputs["Subsurface Radius"].default_value[0] = subsurface_radius[0]
        mat.node_tree.nodes["Principled BSDF"].inputs["Subsurface Radius"].default_value[1] = subsurface_radius[1]
        mat.node_tree.nodes["Principled BSDF"].inputs["Subsurface Radius"].default_value[2] = subsurface_radius[2]
    
    
    if material_data.get("tranmissionDepth"):
        transmission_depth = material_data["tranmissionDepth"]
        mat.node_tree.nodes["Principled BSDF"].inputs["Subsurface Scale"].default_value = transmission_depth
    
    if material_data.get("thinFilmThickness"):
        thin_film_thickness = material_data["thinFilmThickness"]
        mat.node_tree.nodes["Principled BSDF"].inputs["Thin Film Thickness"].default_value = thin_film_thickness
        
        thin_film_ior = material_data.get("thinFilmIor", 1.5)
        mat.node_tree.nodes["Principled BSDF"].inputs["Thin Film IOR"].default_value = thin_film_ior
    
    common_setup(mat, material_data)
        
def create_metallic_material(mat, material_data):
    # delete the default Principled BSDF node and create a metallic bsdf node
    if "Principled BSDF" in mat.node_tree.nodes:
        bsdf_node = mat.node_tree.nodes["Principled BSDF"]
        mat.node_tree.nodes.remove(bsdf_node)

    metallic_bsdf = mat.node_tree.nodes.new("ShaderNodeBsdfMetallic")
    metallic_bsdf.location = (0, 0)
    mat.node_tree.links.new(metallic_bsdf.outputs[0], mat.node_tree.nodes["Material Output"].inputs[0])

    # set the mode to to physical conductor
    metallic_bsdf.fresnel_type = 'PHYSICAL_CONDUCTOR'
    
    metallic_bsdf.inputs["Roughness"].default_value = material_data.get("roughness", 0.5)
        
    i = material_data.get("complexIor", [])

    metallic_bsdf.inputs["IOR"].default_value[0] = i[0]
    metallic_bsdf.inputs["IOR"].default_value[1] = i[2]
    metallic_bsdf.inputs["IOR"].default_value[2] = i[4]
    
    metallic_bsdf.inputs["Extinction"].default_value[0] = i[1]
    metallic_bsdf.inputs["Extinction"].default_value[1] = i[3]
    metallic_bsdf.inputs["Extinction"].default_value[2] = i[5]

    common_setup(mat, material_data)