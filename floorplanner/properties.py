import bpy # type: ignore

props = [
    ('JMFLOORPLANNER_doorHeight', bpy.props.FloatProperty(
        name='doorHeight', default=2.032, subtype='DISTANCE')),
    ('JMFLOORPLANNER_windowHeight', bpy.props.FloatProperty(
        name='windowHeight', default=1.6256, subtype='DISTANCE')),
    ('JMFLOORPLANNER_windowBase', bpy.props.FloatProperty(
        name='windowBase', default=.700, subtype='DISTANCE')),
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
    

def register():
    for (prop_name, prop_value) in props:
        setattr(bpy.types.Scene, prop_name, prop_value)


def unregister():
    for (prop_name, _) in props:
        delattr(bpy.types.Scene, prop_name)