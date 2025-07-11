from multiprocessing import context
import bpy # type: ignore
from . import color_utils
from bpy.props import FloatVectorProperty, PointerProperty, IntProperty, FloatProperty, EnumProperty # type: ignore
from math import pi
from . import assign

HARMONY_TYPES = [
    ('complementary', "Complementary", "2 Colors: Base and its direct complementary."),
    ('near_complementary', "Near Complementary", "2 Colors: Base and a color slightly off its direct complementary."),
    ('split', "Split Complementary", "3 Colors: Base and the two colors adjacent to its direct complementary."),
    ('split_c', "Extended Split Complementary", "4 Colors: Base, its two split complementaries, and the exact complementary of the base."),
    ('analogous', "Analogous", "Multiple Colors: Base and additional colors immediately adjacent on the color wheel."),
    ('analogous_c', "Accented Analogous", "Multiple Colors: An analogous scheme with the addition of the exact complementary accent color."),
    ('triadic', "Triadic", "3 Colors: Three colors equally spaced (120 degrees apart) on the color wheel."),
    ('triadic_c', "Extended Triadic", "4 Colors: A triadic scheme with the addition of the exact complementary of one of the triad's colors."),
    ('square', "Square", "4 Colors: Four colors equally spaced (90 degrees apart) on the color wheel."),
    ('tetradic', "Tetradic", "4 Colors: Two pairs of complementary colors, forming a rectangle on the color wheel."),
    ('monochromatic', "Monochromatic", "Multiple variations (tints, shades, tones) of a single hue."),
    ('achromatic', "Achromatic", "Variations of black, white, and gray (absence of hue).")
]


def update_harmony_colors(self, context):
    scene = context.scene
    props = scene.johnnygizmo_harmony
    base = props.base_color
    mode = props.mode
    count = props.count    

    obj = context.active_object
    if obj and obj.active_material and obj.active_material.use_nodes:
        assign.setNode(obj.active_material, context.scene.johnnygizmo_harmony)

    if bpy.data.palettes.get("Harmony Palette"):
        props.palette = bpy.data.palettes["Harmony Palette"]

    if not props.palette:
        props.palette = color_utils.get_or_create_palette()

    palette = props.palette
    palette.colors.clear()

    if mode == 'complementary':
        colors = color_utils.get_complementary_color(base)

    elif mode == 'near_complementary':
        colors = color_utils.get_near_complementary_colors(base,props.near_complementary_angle)

    elif mode == 'split':
        raw = color_utils.get_split_complementary_colors(base)
        colors = raw[:count]

    elif mode == 'split_c':
        raw = color_utils.get_split_complementary_colors(base)
        raw.append(color_utils.get_single_complementary_color(base))
        colors = raw[:4]

    elif mode == 'analogous':
        raw = color_utils.get_analogous_colors(base, count, degrees = props.analogous_angle)
        countTotal = len(raw)
        colors = raw[:countTotal]

    elif mode == 'analogous_c':
        raw = color_utils.get_analogous_colors(base, count, degrees = props.analogous_angle)
        raw.append(color_utils.get_single_complementary_color(base))
        countTotal = len(raw)
        colors = raw[:countTotal]

    elif mode == 'triadic':
        raw = color_utils.get_triadic_colors(base)
        colors = raw[:count]
    elif mode == 'triadic_c':
        raw = color_utils.get_triadic_colors(base)
        raw.append(color_utils.get_single_complementary_color(base))
        colors = raw[:4]

    elif mode == 'square':
        raw = color_utils.get_square_colors(base)
        colors = raw[:4]

    elif mode == 'tetradic':
        rad = props.tetradic_angle
        raw = color_utils.get_tetradic_colors(base, rad)
        colors = raw[:4]        

    elif mode == 'monochromatic':
        raw = color_utils.get_monochromatic_colors(base, count)
        countTotal = count*2+1
        colors = raw[:countTotal]

    elif mode == 'achromatic':
        raw = color_utils.get_achromatic_colors(base, count)
        countTotal = len(raw)
        colors = raw[:countTotal]
    else:
        colors = []

    for color in colors:
        new = palette.colors.new()
        new.color = color[:3]

type_list = {
            'BSDF_PRINCIPLED',
            'BSDF_METALLIC',
            'BSDF_DIFFUSE',
            'EMISSION',
            'BSDF_GLASS',
            'BSDF_GLOSSY',
            'PRINCIPLED_VOLUME',
            'BSDF_REFRACTION',
            'EEVEE_SPECULAR',
            'BSDF_TRANSLUCENT',
            'SUBSURFACE_SCATTERING',
            'BSDF_TRANSPARENT',
            'VOLUME_ABSORPTION',
            'VOLUME_SCATTER',
            'BSDF_SHEEN',
            'BSDF_TOON',
            'BSDF_RAY_PORTAL',
            'BSDF_HAIR_PRINCIPLED'
        }

def nodeSearch(self, context, edit_text):
    obj = context.active_object
    if obj and obj.active_material and obj.active_material.use_nodes:
        assign.setNode(obj.active_material, context.scene.johnnygizmo_harmony)
        nodes = obj.active_material.node_tree.nodes
        output = [node.name for node in nodes if node.type in type_list and edit_text.lower() in node.name.lower()]
        return output

class HarmonySettings(bpy.types.PropertyGroup):
    mode: EnumProperty(
        name="Harmony Type",
        description="Color harmony rule to use",
        items=HARMONY_TYPES,
        default='complementary',
        update=lambda self, context: update_harmony_colors(self, context)
    ) # type: ignore

    base_color: FloatVectorProperty(
        name="Base Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0, 1.0),
        update=update_harmony_colors
    ) # type: ignore

    palette: PointerProperty(
        name="Harmony Palette",
        type=bpy.types.Palette
    ) # type: ignore


    count: IntProperty(
        name="Number of Outputs",
        description="How many harmony colors to generate",
        default=3,
        min=3,
        max=24,
        update=update_harmony_colors
    ) # type: ignore


    tetradic_angle: FloatProperty(
        name="Tetradic Angle",
        description="Angle between color pairs in degrees (0° to 180°)",
        default=pi/3,
        min=pi/6,
        max=pi * 5 / 6,
        subtype='ANGLE',
        unit='ROTATION',
        update=update_harmony_colors
    ) # type: ignore

    analogous_angle: FloatProperty(
        name="Angle",
        description="Angle between colors",
        default=pi/6,
        subtype='ANGLE',
        precision = 2,
        update=update_harmony_colors
    )     # type: ignore
    target_bsdf_node_name: bpy.props.StringProperty(
        name="Target BSDF Node",
        description="Name of the Principled BSDF or Diffuse BSDF node to target",
        default="Principled BSDF",
        search=nodeSearch

    ) # type: ignore

    near_complementary_angle: FloatProperty(
        name="Angle",
        description="Angle to offset the near complementary color",
        default=0.0872665,
        subtype='ANGLE',
        update=update_harmony_colors
    )     # type: ignore

# Blender Add-on Setup
def register():
    bpy.utils.register_class(HarmonySettings)
    bpy.types.Scene.johnnygizmo_harmony = PointerProperty(type=HarmonySettings)
   

def unregister():
    del bpy.types.Scene.johnnygizmo_harmony
    bpy.utils.unregister_class(HarmonySettings)
