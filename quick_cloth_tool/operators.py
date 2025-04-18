import bpy


class OBJECT_OT_add_quick_cloth_tool(bpy.types.Operator):
    bl_idname = "object.add_quick_cloth_tool"
    bl_label = "Add Quick Cloth Tool"
    bl_description = "Add cloth modifier with pinning group from selected vertices"
    bl_options = {'REGISTER', 'UNDO'}

    use_sewing: bpy.props.BoolProperty(
        name="Enable Sewing",
        description="Enable sewing between cloth vertices",
        default=False
    )

    sewing_force: bpy.props.FloatProperty(
        name="Sewing Force",
        description="Force applied to sewing springs",
        default=5,
        min=0.0,
        precision=4
    )


    use_pressure: bpy.props.BoolProperty(
        name="Enable Pressure",
        description="",
        default=False
    )

    pressure_force: bpy.props.FloatProperty(
        name="Pressure Force",
        description="Force applied to internal pressure",
        default=5,
        min=0.0,
        precision=4
    )


    speed_multiplier: bpy.props.FloatProperty(
        name="Speed Multiplier",
        description="Multiplier for the speed of the cloth simulation",
        default=1,
        min=0.0,
        precision=4
    )

    shrink: bpy.props.FloatProperty(
        name="Shrinking Factor",
        description="Factor to control the shrinking of the cloth",
        default=0,
        min=-1.0,
        max=1.0,
        precision=4
    )


    cloth_mass: bpy.props.FloatProperty(
        name="Vertex Mass",
        description="Mass of the cloth vertices",
        default=3.0,
        min=0.01,
        soft_max=10.0
    )
    collision_quality: bpy.props.IntProperty(
        name="Cloth Quality",
        description="Accuracy of the simulation",
        default=4,
        min=1,
        max=20
    )
    cloth_quality: bpy.props.IntProperty(
        name="Collision Quality",
        description="Accuracy of the collision simulation",
        default=5,
        min=1,
        max=10
    )

    collision_distance: bpy.props.FloatProperty(
        name="Collision Distance",
        description="Distance at which cloth interacts with other objects",
        default=0.001,
        min=0.0,
        precision=4
    )

    use_self_collision: bpy.props.BoolProperty(
        name="Enable Self Collision",
        description="Enable collisions between parts of the cloth itself",
        default=True
    )

    self_collision_distance: bpy.props.FloatProperty(
        name="Self Collision Distance",
        description="Distance at which cloth collides with itself",
        default=0.001,
        min=0.0,
        precision=4
    )

    gravity: bpy.props.FloatProperty(
        name="Gravity",
        description="Strength of the gravity effect on the cloth",
        default=1,
        min=0.0,
        max=1.0,
        precision=4
    )

 
    def execute(self, context):
        obj = context.active_object

        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Please select a mesh object.")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='OBJECT')

        vg = obj.vertex_groups.get("QuickClothToolPinning")
       
        if vg:            
            obj.vertex_groups.remove(vg)
            vg = None

        vg = obj.vertex_groups.new(name="QuickClothToolPinning")        
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.object.mode_set(mode='OBJECT')
        selected_verts = [v for v in obj.data.vertices if v.select]

        if not selected_verts:
            for v in obj.data.vertices:
                vg.add([v.index], 0.0, 'REPLACE')
        else:
            for v in selected_verts:
                vg.add([v.index], 1.0, 'REPLACE')

        if obj.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')


        existing = [m for m in obj.modifiers if m.type == "CLOTH"]
        cloth_mod = None
        if len(existing) > 0:   
            obj.modifiers.remove(existing[0])
            
    
        try:
            cloth_mod = obj.modifiers.new(name="QuickCloth", type='CLOTH')
        except Exception as e:
            self.report({'ERROR'}, f"Could not create Cloth modifier: {e}")
            return {'CANCELLED'}

        if not cloth_mod or cloth_mod.type != 'CLOTH':
            self.report({'ERROR'}, "Cloth modifier creation failed.")
            return {'CANCELLED'}

        if cloth_mod:   
            bpy.ops.object.modifier_move_to_index(modifier="QuickCloth",index=0)
            update_cloth_settings(self, cloth_mod)
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.object.mode_set(mode='OBJECT')   
        return {'FINISHED'}


def update_cloth_settings(self, cloth):
    cloth.settings.vertex_group_mass = "QuickClothToolPinning"
    cloth.settings.mass = self.cloth_mass
    cloth.settings.quality = self.cloth_quality
    cloth.settings.time_scale = self.speed_multiplier

    cloth.settings.shrink_min = self.shrink

    cloth.settings.use_sewing_springs = self.use_sewing
    cloth.settings.sewing_force_max = self.sewing_force
    cloth.settings.use_pressure = self.use_pressure
    cloth.settings.uniform_pressure_force = self.pressure_force
   
    cloth.collision_settings.collision_quality = self.collision_quality
    cloth.collision_settings.distance_min = self.collision_distance
    cloth.collision_settings.use_self_collision = self.use_self_collision
    cloth.collision_settings.self_distance_min = self.self_collision_distance

    cloth.settings.effector_weights.gravity = self.gravity  
    return cloth.settings


class QUICKCLOTH_OT_quick_cloth_apply(bpy.types.Operator):
    """Applies a modifier named 'QuickCloth'."""
    bl_idname = "object.quick_cloth_apply"
    bl_label = "Apply QuickCloth Modifier"
    bl_options = {'REGISTER', 'UNDO'}


    weld: bpy.props.BoolProperty(
        name="Weld Loose Edges",
        description="Weld loose edges after applying the cloth modifier",
        default=True
    )

    distance: bpy.props.FloatProperty(
        name="Weld Distance",
        description="Distance for the weld modifier",
        default=.01,
        min=0.0,
        max=1.0,
        precision=4
    )


    def execute(self, context):
        obj = context.active_object
        if obj:
            bpy.ops.object.mode_set(mode='OBJECT')   

            bpy.ops.object.modifier_apply(modifier="QuickCloth")
            
            if self.weld:
                weld = obj.modifiers.new(name="QuickClothWeld", type='WELD')
                weld.mode = 'CONNECTED'
                weld.loose_edges = True
                weld.merge_threshold = self.distance
                bpy.ops.object.modifier_apply(modifier="QuickClothWeld")    
           

            vg = obj.vertex_groups.get("QuickClothToolPinning")
            if vg:
                obj.vertex_groups.remove(vg)
            self.report({'INFO'}, "Applied 'QuickCloth' modifier.")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No object selected.")
            return {'CANCELLED'}
        
class QUICKCLOTH_OT_quick_cloth_remove(bpy.types.Operator):
    """Removes a modifier named 'QuickCloth'."""
    bl_idname = "object.quick_cloth_remove"
    bl_label = "Remove QuickCloth Modifier"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        obj = context.active_object
        if obj:
            bpy.ops.object.mode_set(mode='OBJECT')   

            bpy.ops.object.modifier_remove(modifier="QuickCloth")
            bpy.ops.object.modifier_remove(modifier="QuickClothWeld")             

            vg = obj.vertex_groups.get("QuickClothToolPinning")
            if vg:
                obj.vertex_groups.remove(vg)
            self.report({'INFO'}, "Applied 'QuickCloth' modifier.")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No object selected.")
            return {'CANCELLED'}


class QUICKCLOTH_OT_quick_cloth_stitch_edgeloops(bpy.types.Operator):
    """Applies a modifier named 'QuickCloth'."""
    bl_idname = "object.quick_cloth_stitch_edgeloops"
    bl_label = "Add Stiching Between Edge Loops"
    def execute(self, context):
        obj = context.active_object
        if obj:
            bpy.ops.object.mode_set(mode='EDIT')   

            bpy.ops.mesh.bridge_edge_loops()
            bpy.ops.mesh.delete(type='ONLY_FACE')
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No object selected.")
            return {'CANCELLED'}      

class QUICKCLOTH_OT_quick_cloth_add_collision(bpy.types.Operator):
    """Adds a collision modifier to the selected object."""
    bl_idname = "object.quick_cloth_add_collision"
    bl_label = "Add Collision Modifier"
    bl_options = {'REGISTER', 'UNDO'}
    
  
    
    def execute(self, context):
        obj = context.active_object
        if obj:
            bpy.ops.object.mode_set(mode='OBJECT')   

            existing = [m for m in obj.modifiers if m.type == "COLLISION"]
            if len(existing) == 0:   
                obj.modifiers.new(name="QuickClothCollision", type='COLLISION')
                bpy.ops.object.modifier_move_to_index(modifier="QuickClothCollision",index=0)
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No object selected.")
            return {'CANCELLED'}            


def register():
    bpy.utils.register_class(OBJECT_OT_add_quick_cloth_tool)
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_apply)
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_remove)
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_stitch_edgeloops)
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_add_collision)

def unregister():
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_add_collision)
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_stitch_edgeloops)
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_remove)
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_apply)
    bpy.utils.unregister_class(OBJECT_OT_add_quick_cloth_tool)
    