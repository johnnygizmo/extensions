import bpy # type: ignore

props = [
       
    ('JMFLOORPLANNER_edgeLength', bpy.props.FloatProperty(
        name='edgeLength', default=1, subtype='DISTANCE')),
    ('JMFLOORPLANNER_wallWidth', bpy.props.FloatProperty(
        name='wallWidth', default=.15, subtype='DISTANCE')),
    ('JMFLOORPLANNER_wallCenter', bpy.props.FloatProperty(
        name='wallCenter', default=0, subtype='DISTANCE')),
    ('JMFLOORPLANNER_wallExt1', bpy.props.FloatProperty(
        name='wallExt1', default=0, subtype='DISTANCE')),
    ('JMFLOORPLANNER_wallExt2', bpy.props.FloatProperty(
        name='wallExt2', default=0, subtype='DISTANCE')),
]
    

class MyToolSettings(bpy.types.PropertyGroup):
    door_height: bpy.props.FloatProperty(name="Float", default=1.0,subtype='DISTANCE') # type: ignore
    door_width:  bpy.props.FloatProperty(name="Float", default=1.0,subtype='DISTANCE')     # type: ignore
    window_height: bpy.props.FloatProperty(name="Float", default=1.6256,subtype='DISTANCE') # type: ignore
    window_width:  bpy.props.FloatProperty(name="Float", default=.700,subtype='DISTANCE')     # type: ignore
    window_base:   bpy.props.FloatProperty(name="Float", default=1.0,subtype='DISTANCE')     # type: ignore

def register():
    bpy.utils.register_class(MyToolSettings)
    for (prop_name, prop_value) in props:
        setattr(bpy.types.Scene, prop_name, prop_value)
    bpy.types.Scene.johnnygizmo_floorplanner_tool_settings = bpy.props.PointerProperty(type=MyToolSettings)



def unregister():
    bpy.utils.unregister_class(MyToolSettings)
    del bpy.types.Scene.johnnygizmo_floorplanner_tool_settings
    for (prop_name, _) in props:
        delattr(bpy.types.Scene, prop_name)