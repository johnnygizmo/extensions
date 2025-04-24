# ui.py
import bpy
import mathutils


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
        row = layout.row()
        col1 = row.column()
        col1.operator("object.add_quick_cloth_tool", text="Add")
        col2 = row.column()
        col2.operator("object.quick_cloth_apply", text="Apply")
        col3 = row.column()
        col3.operator("object.quick_cloth_remove", text="Remove")

        layout.label(text="Quick Pillow")
        row = layout.row()
        col1 = row.column()
        col1.operator("object.add_quick_pillow", text="Add")
        col2 = row.column()
        col2    .operator("object.apply_quick_pillow", text="Apply")


        layout.label(text="Cloth Drag")
        row = layout.row()
        col1 = row.column()
        col1.operator("object.quickcloth_clothdrag", text="Add")
        col2 = row.column()
        col2.operator("object.quickcloth_clothdrag_apply", text="Apply") 

        layout.label(text="Collision")
        row = layout.row()
        col1 = row.column()
        col1.operator("object.quick_cloth_add_collision",text="Add")
        col2 = row.column()
        col2.operator("object.quick_cloth_rem_collision",text="Remove")

        layout.label(text="Stitching")

        layout.operator("object.quick_cloth_stitch_edgeloops", text="Edge Loops to Stitch")
        layout.operator("object.quick_cloth_stitch_vertring", text="Vertring to Alternating Cinch Stitch")
        layout.operator("object.quick_cloth_delete_loose_edges", text="Delete Loose Edges")

        layout.label(text="Gravity")

        row = layout.row()
        col1 = row.column()
        col1.prop(context.scene, "use_gravity", text="Enabled")
        col2 = row.column()
        if context.scene.gravity == mathutils.Vector((0, 0, -9.8)):
            col2.label(text="Current: Down")
        elif context.scene.gravity == mathutils.Vector((0, 0, 9.8)):
            col2.label(text="Current: Up")
        elif context.scene.gravity == mathutils.Vector((-9.8, 0, 0)):
            col2.label(text="Current: Left")
        elif context.scene.gravity == mathutils.Vector((9.8, 0, 0)):
            col2.label(text="Current: Right")
        elif context.scene.gravity == mathutils.Vector((0, 9.8, 0)):
            col2.label(text="Current: Push")
        elif context.scene.gravity == mathutils.Vector((0, -9.8, 0)):
            col2.label(text="Current: Pull")
        else:
            col2.label(text="Current: Other")
        
        row = layout.row()
        col1 = row.column()
        col1.operator("object.set_gravity", text="Up").direction = "Up"
        col1.operator("object.set_gravity", text="Down").direction = "Down"

        col2 = row.column()
        col2.operator("object.set_gravity", text="Left").direction = "Left"
        col2.operator("object.set_gravity", text="Right").direction = "Right"

        col3 = row.column()
        col3.operator("object.set_gravity", text="Push").direction = "Push"
        col3.operator("object.set_gravity", text="Pull").direction = "Pull"

        
def register():
    bpy.utils.register_class(QUICK_SIM_PT_panel)

def unregister():
    bpy.utils.unregister_class(QUICK_SIM_PT_panel)

if __name__ == "__main__":
    register()