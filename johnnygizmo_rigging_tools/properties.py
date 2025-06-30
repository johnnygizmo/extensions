import bpy



class JohnnyGizmoProperties(bpy.types.PropertyGroup):
    
    selected_object: bpy.props.PointerProperty(
        name="Selected Object",
        description="Selected Object",
        type=bpy.types.Object,
    )
    selected_object_2: bpy.props.PointerProperty(
        name="Selected Object 2" ,
        description="Selected Object 2",
        type=bpy.types.Object,
    )  

    selected_bone: bpy.props.StringProperty(
        name="Selected Bone",
        description="Selected Bone",
    )  
    selected_bone_2: bpy.props.StringProperty(
        name="Selected Bone 2",
        description="Selected Bone 2",
    )        

    def clear(self):
        """Clear all properties"""
        self.selected_object = None
        self.selected_object_2 = None
        self.selected_bone = ""
        self.selected_bone_2 = ""
        
def register():
    bpy.utils.register_class(JohnnyGizmoProperties)
    bpy.types.Scene.johnnygizmo_rigging_tools_properties = bpy.props.PointerProperty(type=JohnnyGizmoProperties)

def unregister():
    bpy.utils.unregister_class(JohnnyGizmoProperties)
    del bpy.types.Scene.johnnygizmo_rigging_tools_properties
