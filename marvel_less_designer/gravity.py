import bpy

class OBJECT_OT_set_gravity(bpy.types.Operator):
    """Set Gravity Direction"""
    bl_idname = "object.set_gravity"
    bl_label = "Set Gravity"
    bl_options = {'REGISTER', 'UNDO'}
    

    direction: bpy.props.StringProperty(
        name="Direction",
        description="Direction of the gravity force",
        default="Down",
    ) # type: ignore

    def execute(self, context):
        if self.direction == "Up":
            context.scene.gravity = (0, 0, 9.8)
        elif self.direction == "Down":
            context.scene.gravity = (0, 0, -9.8)
        elif self.direction == "Left":
            context.scene.gravity = (-9.8, 0, 0)
        elif self.direction == "Right":
            context.scene.gravity = (9.8, 0, 0)
        elif self.direction == "Push":
            context.scene.gravity = (0, 9.8, 0)
        elif self.direction == "Pull":
            context.scene.gravity = (0, -9.8, 0)
        else:
            context.scene.gravity = (0, 0, -9.8)

        return {'FINISHED'}
      


def register():
    bpy.utils.register_class(OBJECT_OT_set_gravity)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_set_gravity)
    