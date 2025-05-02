import bpy # type: ignore

class QUICKCLOTH_OT_quick_cloth_add_collision(bpy.types.Operator):
    """Adds a collision modifier to the selected object."""
    bl_idname = "object.quick_cloth_add_collision"
    bl_label = "Add Quick Collision"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) != 0 and context.active_object != None and context.active_object.type == 'MESH' 
    

    damping: bpy.props.FloatProperty(
        name="Damping",
        description="Damping",
        default=.1,
        min=0.0,
        max= 1,
    )  # type: ignore
    friction: bpy.props.FloatProperty(
        name="Friction",
        description="Friction",
        default=5,
        min=0.0,
        max= 80.0,
    )  # type: ignore
    thickness_outer: bpy.props.FloatProperty(
        name="Thickness Outer",
        description="Thickness Outer",
        default=0.02,
        min=0.001,
        max= 1.0,  
    )  # type: ignore
    single: bpy.props.BoolProperty(
        name="Single Sided",
        description="Single Sided",
        default=True
    )  # type: ignore
    override:bpy.props.BoolProperty(
        name="Override Normals",
        description="Override Normals",
        default=False
    )  # type: ignore

    def execute(self, context):
        obj = context.active_object
        if obj:
            bpy.ops.object.mode_set(mode='OBJECT')   

            existing = [m for m in obj.modifiers if m.type == "COLLISION"]
            if len(existing) == 1:
                bpy.ops.object.modifier_remove(modifier=existing[0].name)
        
            coll = obj.modifiers.new(name="QuickClothCollision", type='COLLISION')
            coll.settings.damping = self.damping
            coll.settings.thickness_outer = self.thickness_outer
            coll.settings.cloth_friction = self.friction
            coll.settings.use_culling = self.single
            coll.settings.use_normal = self.override

            bpy.ops.object.modifier_move_to_index(modifier="QuickClothCollision",index=0)
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No object selected.")
            return {'CANCELLED'}            

class QUICKCLOTH_OT_quick_cloth_rem_collision(bpy.types.Operator):
    """Remove a collision modifier to the selected object."""
    bl_idname = "object.quick_cloth_rem_collision"
    bl_label = "Remove Quick Collision"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) != 0 and context.active_object != None and context.active_object.type == 'MESH'
    
    def execute(self, context):
        obj = context.active_object
        if obj:
            bpy.ops.object.mode_set(mode='OBJECT')   
            bpy.ops.object.modifier_remove(modifier="QuickClothCollision")

            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No object selected.")
            return {'CANCELLED'}            


def register():
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_add_collision)
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_rem_collision)

def unregister():
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_rem_collision)
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_add_collision)