# ui.py
import bpy # type: ignore
import mathutils # type: ignore


class MARVEL_LESS_DESIGNER_PT_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Marvel-Less Designer"
    bl_idname = "OBJECT_PT_marvel_less_designer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Marvel-Less Designer" 

    def draw(self, context):
        layout = self.layout
        layout.label(text="Stitching")        
        layout.operator("object.marvel_less_set_stitch", text="Add Next Stitch")
        layout.operator("object.marvel_less_clear_stitch", text="Clear Stitching")
        

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
        col2 = row.column()
        col2.operator("object.set_gravity", text="Left").direction = "Left"
        col2.operator("object.set_gravity", text="Right").direction = "Right"

        col3 = row.column()
        col3.operator("object.set_gravity", text="Push").direction = "Push"
        col3.operator("object.set_gravity", text="Pull").direction = "Pull"

        col1 = row.column()
        col1.operator("object.set_gravity", text="Up").direction = "Up"
        col1.operator("object.set_gravity", text="Down").direction = "Down"


        layout.prop(context.scene, "gravity")



        
def register():
    bpy.utils.register_class(MARVEL_LESS_DESIGNER_PT_panel)

def unregister():
    bpy.utils.unregister_class(MARVEL_LESS_DESIGNER_PT_panel)

if __name__ == "__main__":
    register()