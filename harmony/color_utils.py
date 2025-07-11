import bpy
import colorsys
from bpy.props import FloatVectorProperty, PointerProperty
from math import pow, pi

def linear_to_srgb(c):
    if c <= 0.0031308:
        return 12.92 * c
    else:
        return 1.055 * pow(c, 1.0 / 2.4) - 0.055

def srgb_to_linear(c):
    if c <= 0.04045:
        return c / 12.92
    else:
        return pow((c + 0.055) / 1.055, 2.4)

def convert_linear_rgb_to_srgb(linear_rgb):
    return [linear_to_srgb(c) for c in linear_rgb]

def convert_srgb_to_linear_rgb(srgb_rgb):
    return [srgb_to_linear(c) for c in srgb_rgb]


# Color Harmony Math
def get_complementary_color(color):
    srgb_color = convert_linear_rgb_to_srgb(color[:3])
    h, s, v = colorsys.rgb_to_hsv(*srgb_color)
    h = (h + 0.5) % 1.0
    complementary_srgb = colorsys.hsv_to_rgb(h, s, v)
    
    return [
        (srgb_color[:3]), 
        (*convert_srgb_to_linear_rgb(complementary_srgb), 1.0)
    ]

def get_split_complementary_colors(color):
    srgb_color = convert_linear_rgb_to_srgb(color[:3])
    h, s, v = colorsys.rgb_to_hsv(*srgb_color)
    h1 = (h + 5/12) % 1.0  
    h2 = (h - 5/12) % 1.0 
    split1_srgb = colorsys.hsv_to_rgb(h1, s, v)
    split2_srgb = colorsys.hsv_to_rgb(h2, s, v)

    return [
        (*convert_srgb_to_linear_rgb(split1_srgb), 1.0),
        (srgb_color[:3]), 
        (*convert_srgb_to_linear_rgb(split2_srgb), 1.0)
    ]

def get_analogous_colors(color, count=3, degrees= 1/12):
    if count < 1: 
        count = 1
    if count % 2 == 0: 
        count += 1 

    srgb_base_color = convert_linear_rgb_to_srgb(color[:3])
    h, s, v = colorsys.rgb_to_hsv(*srgb_base_color)
    step = 0
    if degrees != 0:
        step = 1 / ((pi*2) / degrees)

    results = [None] * count 
    center_index = count // 2 
    results[center_index] = (*color[:3], 1.0)

    for i in range(count):
        if i == center_index:
            continue 
        offset = i - center_index 
        shifted_h = (h + offset * step) % 1.0
        srgb_rgb = colorsys.hsv_to_rgb(shifted_h, s, v)
        results[i] = (*convert_srgb_to_linear_rgb(srgb_rgb), 1.0)

    return results


def get_triadic_colors(color):
    srgb_color = convert_linear_rgb_to_srgb(color[:3])
    h, s, v = colorsys.rgb_to_hsv(*srgb_color)
    
    triadic1_srgb = colorsys.hsv_to_rgb((h + 1/3) % 1.0, s, v)
    triadic2_srgb = colorsys.hsv_to_rgb((h - 1/3) % 1.0, s, v)

    return [
        (*convert_srgb_to_linear_rgb(triadic1_srgb), 1.0),
        (srgb_color[:3]), # Original base color (linear)
        (*convert_srgb_to_linear_rgb(triadic2_srgb), 1.0)
    ]

def get_tetradic_colors(color, rad=3.14159/3):
    srgb_color = convert_linear_rgb_to_srgb(color[:3])
    angle_deg = rad * 180 / 3.14159  # Convert radians to degrees
    h, s, v = colorsys.rgb_to_hsv(*srgb_color)
    angle = angle_deg / 360.0
    h1 = h
    h2 = (h + angle) % 1.0
    h3 = (h + 0.5) % 1.0         
    h4 = (h3 + angle) % 1.0      

    result = [
        (srgb_color[:3]),
        (*convert_srgb_to_linear_rgb(colorsys.hsv_to_rgb(h2, s, v)), 1.0),
        (*convert_srgb_to_linear_rgb(colorsys.hsv_to_rgb(h3, s, v)), 1.0),
        (*convert_srgb_to_linear_rgb(colorsys.hsv_to_rgb(h4, s, v)), 1.0)
    ]
    return result

def get_square_colors(color):
    srgb_color = convert_linear_rgb_to_srgb(color[:3])
    h, s, v = colorsys.rgb_to_hsv(*srgb_color)
    
    results = []
    results.append((*srgb_color[:3], 1.0)) 

    for i in range(1, 4): 
        srgb_rgb = colorsys.hsv_to_rgb((h + 0.25 * i) % 1.0, s, v)
        results.append((*convert_srgb_to_linear_rgb(srgb_rgb), 1.0))
        
    return results

def get_monochromatic_colors(color, count=1):
    srgb_color = convert_linear_rgb_to_srgb(color[:3])
    h, s, v = colorsys.rgb_to_hsv(*srgb_color)
    results = []

    results.append((srgb_color[:3]))
    for i in range(1,count):
        sat = max(0.0, s - i * (s / (count + 1)))
        val = max(0.0, v - i * (v / (count + 1)))
        srgb_rgb = colorsys.hsv_to_rgb(h, sat, val)
        results.append((*convert_srgb_to_linear_rgb(srgb_rgb), 1.0))
    return results

def get_or_create_palette(name="Harmony Palette"):
    if name in bpy.data.palettes:
        return bpy.data.palettes[name]
    return bpy.data.palettes.new(name)

