import bpy
from . import harmony_colors

def colorControl(parent, palette, idx, scale=1.0):
    col = parent.column()
    col.alignment = "CENTER"
    c = palette.colors[idx].color
    # color.append(1)
    subrow = col.row(align=True)
    subrow.alignment = "CENTER"
    subrow.scale_x = 3 * scale
    subrow.scale_y = 1
    if palette.colors.active == palette.colors[idx]:
        subrow.scale_x = 3 * scale
        subrow.scale_y = 1
    subrow.prop(palette.colors[idx], "color", text="")
    
    subrow = col.row(align=True)
    subrow.alignment = "CENTER"
    icon = "BLANK1"
    if palette.colors.active == palette.colors[idx]:
        icon = "PMARKER_ACT"
    op = subrow.operator(
        "johnnygizmo_colorharmony.set_active_palette_color",
        text="",
        icon=icon,
        emboss=True,
    )
    op.index = idx


def color_palette(layout, palette, mode, steps):
    count = len(palette.colors)
    pattern = harmony_colors.get_pattern(mode, steps)
    placed = 0
    position = 0
    rw = layout.row(align=True)
    while placed < count:
        action = pattern[position % len(pattern)]
        if action == 0:
            rw.separator(factor=3, type="SPACE")
            position += 1
        elif action == 1:
            colorControl(rw, palette, placed, harmony_colors.TYPE_PATTERNS[mode][1])
            placed += 1
            position += 1
        elif action == 2:
            rw = layout.row(align=True)
            position += 1
