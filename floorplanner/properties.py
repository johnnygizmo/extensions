import bpy # type: ignore
   
class MyToolSettings(bpy.types.PropertyGroup):
    door_height: bpy.props.FloatProperty(name="Float", default=1.0,subtype='DISTANCE') # type: ignore
    door_width:  bpy.props.FloatProperty(name="Float", default=1.0,subtype='DISTANCE')     # type: ignore
    window_height: bpy.props.FloatProperty(name="Float", default=1.6256,subtype='DISTANCE') # type: ignore
    window_width:  bpy.props.FloatProperty(name="Float", default=.700,subtype='DISTANCE')     # type: ignore
    window_base:   bpy.props.FloatProperty(name="Float", default=1.0,subtype='DISTANCE')     # type: ignore
    edge_length: bpy.props.FloatProperty(name="Float", default=1.0,subtype='DISTANCE') # type: ignore
    wall_width: bpy.props.FloatProperty(name="Float", default=.15,subtype='DISTANCE') # type: ignore
    wall_center: bpy.props.FloatProperty(name="Float", default=0,subtype='DISTANCE') # type: ignore
    wall_ext1: bpy.props.FloatProperty(name="Float", default=0,subtype='DISTANCE') # type: ignore
    wall_ext2: bpy.props.FloatProperty(name="Float", default=0,subtype='DISTANCE') # type: ignore

def register():
    bpy.utils.register_class(MyToolSettings)
    bpy.types.Scene.johnnygizmo_floorplanner_tool_settings = bpy.props.PointerProperty(type=MyToolSettings)



def unregister():
    bpy.utils.unregister_class(MyToolSettings)
    del bpy.types.Scene.johnnygizmo_floorplanner_tool_settings