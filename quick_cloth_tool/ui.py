# ui.py
import bpy

class QUICK_SIM_PT_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Quick Sim"
    bl_idname = "OBJECT_PT_quick_sim"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Quick Cloth Tool" 

    def draw(self, context):
        layout = self.layout
        layout.label(text="Quick Cloth")
        layout.operator("object.add_quick_cloth_tool", text="Add")
        layout.operator("object.quick_cloth_apply", text="Apply")
        layout.operator("object.quick_cloth_remove", text="Remove")
        layout.separator() 
        layout.operator("object.quick_cloth_stitch_edgeloops", text="Edge Loops to Stitch")
        layout.separator()
        layout.operator("object.quick_cloth_add_collision")
        layout.label(text="Quick Pillow")
        layout.operator("object.add_quick_pillow", text="Add")
        layout.operator("object.apply_quick_pillow", text="Apply")


def register():
    bpy.utils.register_class(QUICK_SIM_PT_panel)

def unregister():
    bpy.utils.unregister_class(QUICK_SIM_PT_panel)

if __name__ == "__main__":
    register()