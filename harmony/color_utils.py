import bpy
import colorsys
from bpy.props import FloatVectorProperty, PointerProperty


# Color Harmony Math
def get_complementary_color(color):
    h, s, v = colorsys.rgb_to_hsv(*color[:3])
    h = (h + 0.5) % 1.0
    return [
        (color[:3]),
        (*colorsys.hsv_to_rgb(h, s, v), 1.0)
    ]

def get_split_complementary_colors(color):
    h, s, v = colorsys.rgb_to_hsv(*color[:3])
    h1 = (h + 5/12) % 1.0  # +150°
    h2 = (h - 5/12) % 1.0  # -150°
    return [
        (*colorsys.hsv_to_rgb(h1, s, v), 1.0),
        (color[:3]),
        (*colorsys.hsv_to_rgb(h2, s, v), 1.0)
    ]

def get_analogous_colors(color, count=3):
    import colorsys

    if count < 3 or count % 2 == 0:
        raise ValueError("Count must be an odd number greater or equal to 3")

    h, s, v = colorsys.rgb_to_hsv(*color[:3])
    step = 1 / 12  # 30 degrees per step, tweak if you want a different angle

    center_index = count // 2  # middle index

    results = []
    for i in range(count):
        offset = i - center_index  # negative to positive, e.g. for count=5: -2,-1,0,1,2
        if offset == 0:
            # Exactly the base color, no conversion
            results.append((*color[:3], 1.0))
        else:
            shifted_h = (h + offset * step) % 1.0
            rgb = colorsys.hsv_to_rgb(shifted_h, s, v)
            results.append((*rgb, 1.0))

    return results


def get_triadic_colors(color):
    h, s, v = colorsys.rgb_to_hsv(*color[:3])
    return [
        (*colorsys.hsv_to_rgb((h + 1/3) % 1.0, s, v), 1.0),
        (color[:3]),
        (*colorsys.hsv_to_rgb((h - 1/3) % 1.0, s, v), 1.0)
    ]

def get_tetradic_colors(color, rad=3.14159/3):
    import colorsys

    angle_deg = rad * 180 / 3.14159  # Convert radians to degrees

    h, s, v = colorsys.rgb_to_hsv(*color[:3])

    # Convert degrees to hue fraction (0–1)
    angle = angle_deg / 360.0

    # Create the rectangle
    h1 = h
    h2 = (h + angle) % 1.0
    h3 = (h + 0.5) % 1.0           # complement of h
    h4 = (h3 + angle) % 1.0        # complement of h2

    result = [
        (*colorsys.hsv_to_rgb(h1, s, v), 1.0),
        (*colorsys.hsv_to_rgb(h2, s, v), 1.0),
        (*colorsys.hsv_to_rgb(h3, s, v), 1.0),
        (*colorsys.hsv_to_rgb(h4, s, v), 1.0)
    ]
    return result

def get_square_colors(color):
    h, s, v = colorsys.rgb_to_hsv(*color[:3])
    return [
        (*colorsys.hsv_to_rgb((h + 0.25 * i) % 1.0, s, v), 1.0)
        for i in range(4)
    ]



def get_monochromatic_colors(color, count=5):
    import colorsys

    h, s, v = colorsys.rgb_to_hsv(*color[:3])
    result = []

    # Start with the original color, then step down in saturation and value
    for i in range(count):
        sat = max(0.0, s - i * (s / (count + 1)))
        val = max(0.0, v - i * (v / (count + 1)))
        rgb = colorsys.hsv_to_rgb(h, sat, val)
        result.append((*rgb, 1.0))
    return result

class COLORHARMONY_OT_ApplyColor(bpy.types.Operator):
    bl_idname = "colorharmony.apply_color"
    bl_label = "Apply Color"
    bl_description = "Apply this color to the active material"

    color: bpy.props.FloatVectorProperty(size=4, subtype='COLOR')

    def execute(self, context):
        obj = context.object
        mat = obj.active_material if obj else None

        if mat and mat.use_nodes:
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs["Base Color"].default_value = self.color
                self.report({'INFO'}, "Color applied!")
            else:
                self.report({'WARNING'}, "Principled BSDF not found.")
        else:
            self.report({'WARNING'}, "No material or nodes found.")

        return {'FINISHED'}

def get_or_create_palette(name="Harmony Palette"):
    if name in bpy.data.palettes:
        return bpy.data.palettes[name]
    return bpy.data.palettes.new(name)


def register():
    bpy.utils.register_class(COLORHARMONY_OT_ApplyColor)

def unregister():
    bpy.utils.unregister_class(COLORHARMONY_OT_ApplyColor)