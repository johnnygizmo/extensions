import bpy
from . import color_utils
from bpy.props import FloatVectorProperty, PointerProperty, IntProperty, FloatProperty
from math import pi

# Color Storage Group
from bpy.props import EnumProperty

HARMONY_TYPES = [
    ('complementary', "Complementary", ""),
    ('split', "Split Complementary", ""),
    ('analogous', "Analogous", ""),
    ('triadic', "Triadic", ""),
    ('square', "Square", ""),
    ('tetradic', "Tetradic", ""),
    ('monochromatic', "Monochromatic", "")
]

def check_and_update_harmony_colors(scene):
    base = scene.johnnygizmo_harmony_base_color
    mode = scene.johnnygizmo_harmony_colors.harmony_mode

    # if bpy.data.palettes.get("Harmony Palette"):
    #     scene.johnnygizmo_harmony_palette = bpy.data.palettes["Harmony Palette"]

    if not scene.johnnygizmo_harmony_palette:
        scene.johnnygizmo_harmony_palette = color_utils.get_or_create_palette()

    palette = scene.johnnygizmo_harmony_palette
    palette.colors.clear()

    count = scene.johnnygizmo_harmony_count
    rad = scene.johnnygizmo_tetradic_angle
    angle = scene.johnnygizmo_analogous_angle

    if mode == 'complementary':
        colors = color_utils.get_complementary_color(base)

    elif mode == 'split':
        raw = color_utils.get_split_complementary_colors(base)
        colors = raw[:count]

    elif mode == 'analogous':
        raw = color_utils.get_analogous_colors(base, count, degrees = angle)
        countTotal = len(raw)
        colors = raw[:countTotal]

    elif mode == 'triadic':
        raw = color_utils.get_triadic_colors(base)
        colors = raw[:count]

    elif mode == 'square':
        raw = color_utils.get_square_colors(base)
        colors = raw[:count]

    elif mode == 'tetradic':
        
        raw = color_utils.get_tetradic_colors(base, rad)
        colors = raw[:count]        

    elif mode == 'monochromatic':
        raw = color_utils.get_monochromatic_colors(base, count)
        countTotal = count*2+1
        colors = raw[:countTotal]
    else:
        colors = []

    for color in colors:
        new = palette.colors.new()
        new.color = color[:3]

def update_harmony_colors(self, context):
    check_and_update_harmony_colors(context.scene)

class HarmonyColors(bpy.types.PropertyGroup):
    harmony_mode: EnumProperty(
        name="Harmony Type",
        description="Color harmony rule to use",
        items=HARMONY_TYPES,
        default='complementary',
        update=lambda self, context: update_harmony_colors(self, context)
    )


# Blender Add-on Setup
def register():
    bpy.utils.register_class(HarmonyColors)

    bpy.types.Scene.johnnygizmo_harmony_base_color = FloatVectorProperty(
        name="Base Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0, 1.0),
        update=update_harmony_colors
    )
    bpy.types.Scene.johnnygizmo_harmony_colors = PointerProperty(type=HarmonyColors)

    bpy.types.Scene.johnnygizmo_harmony_palette = PointerProperty(
        name="Harmony Palette",
        type=bpy.types.Palette
    )
    
    bpy.types.Scene.johnnygizmo_harmony_count = IntProperty(
        name="Number of Outputs",
        description="How many harmony colors to generate",
        default=3,
        min=3,
        max=12,
        update=update_harmony_colors
    )

    bpy.types.Scene.johnnygizmo_tetradic_angle = FloatProperty(
        name="Tetradic Angle",
        description="Angle between color pairs in degrees (0° to 180°)",
        default=pi/3,
        min=pi/6,
        max=pi * 5 / 6,
        subtype='ANGLE',
        unit='ROTATION',
        update=update_harmony_colors
    )

    bpy.types.Scene.johnnygizmo_analogous_angle = FloatProperty(
        name="Angle",
        description="Angle between colors",
        default=pi/6,
        subtype='ANGLE',
        precision = 2,
        update=update_harmony_colors
    )    

def unregister():
    del bpy.types.Scene.johnnygizmo_harmony_base_color
    del bpy.types.Scene.johnnygizmo_harmony_colors
    del bpy.types.Scene.johnnygizmo_harmony_palette
    del bpy.types.Scene.johnnygizmo_harmony_count
    del bpy.types.Scene.johnnygizmo_tetradic_angle
    bpy.utils.unregister_class(HarmonyColors)
