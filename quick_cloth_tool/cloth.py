import bpy # type: ignore

class OBJECT_OT_add_quick_cloth_tool(bpy.types.Operator):
    bl_idname = "object.add_quick_cloth_tool"
    bl_label = "Add Quick Cloth Tool"
    bl_description = "Add cloth modifier with pinning group from selected vertices"
    bl_options = {'REGISTER', 'UNDO'}

    def set_label(self, value):
        return None

    cloth_quality: bpy.props.IntProperty(
        name="Quality Steps",
        description="Accuracy of the collision simulation",
        default=5,
        min=1,
        max=10
    ) # type: ignore


    speed_multiplier: bpy.props.FloatProperty(
        name="Speed Multiplier",
        description="Multiplier for the speed of the cloth simulation",
        default=1,
        min=0.0,
        precision=4
    ) # type: ignore # type: ignore

    cloth_mass: bpy.props.FloatProperty(
        name="Vertex Mass",
        description="Mass of the cloth vertices",
        default=3.0,
        min=0.01,
        soft_max=10.0
    ) # type: ignore
    air_viscosity: bpy.props.FloatProperty(
        name="Air Viscosity",
        description="Air Viscosity",
        default=1.0,
        min=0.00,
        soft_max=10.0
    ) # type: ignore

    stiffness: bpy.props.StringProperty(
        name="",
        description="",
        default="Stiffness",
        set=set_label
    )  # type: ignore



    stension: bpy.props.FloatProperty(
        name="Tension",
        description="Tension",
        default=15.0,
        min=0.00
    ) # type: ignore
    scompression: bpy.props.FloatProperty(
        name="Compression",
        description="Comspression",
        default=15.0,
        min=0.00
    ) # type: ignore
    sshear: bpy.props.FloatProperty(
        name="Shear",
        description="Shear",
        default=5.0,
        min=0.00
    ) # type: ignore

    sbending: bpy.props.FloatProperty(
        name="Bending",
        description="Bending",
        default=1.0,
        min=0.00
    ) # type: ignore
    damping: bpy.props.StringProperty(
        name="",
        description="",
        default="Damping",
        set=set_label
    )  # type: ignore
    dtension: bpy.props.FloatProperty(
        name="Tension",
        description="Tension",
        default=15.0,
        min=0.00
    ) # type: ignore
    dcompression: bpy.props.FloatProperty(
        name="Compression",
        description="Comspression",
        default=15.0,
        min=0.00
    ) # type: ignore
    dshear: bpy.props.FloatProperty(
        name="Shear",
        description="Shear",
        default=5.0,
        min=0.00
    ) # type: ignore
    dbending: bpy.props.FloatProperty(
        name="Bending",
        description="Bending",
        default=1.0,
        min=0.00
    ) # type: ignore
    springs_label: bpy.props.StringProperty(
        name="",
        description="",
        default="Internal Springs",
        set=set_label
    )  # type: ignore
    use_springs: bpy.props.BoolProperty(
        name="Enable Springs",
        description="Enable internal volume structure",
        default=False
    ) # type: ignore
    pressure_label: bpy.props.StringProperty(
        name="",
        description="",
        default="Pressure",
        set=set_label
    )      # type: ignore
    use_pressure: bpy.props.BoolProperty(
        name="Enable Pressure",
        description="",
        default=False
    ) # type: ignore

    pressure_force: bpy.props.FloatProperty(
        name="Pressure Force",
        description="Force applied to internal pressure",
        default=5,
        min=0.0,
        precision=4
    ) # type: ignore
    shape_label: bpy.props.StringProperty(
        name="",
        description="",
        default="Shape",
        set=set_label
    )  # type: ignore
    pinning_stiffness: bpy.props.FloatProperty(
        name="Pinning Stiffness",
        description="Pin Spring Stiffness",
        default=1,
        min=0.0,
        precision=4,
        max=50
    )         # type: ignore
    use_sewing: bpy.props.BoolProperty(
        name="Enable Sewing",
        description="Enable sewing between cloth vertices",
        default=True
    ) # type: ignore
    sewing_force: bpy.props.FloatProperty(
        name="Sewing Force",
        description="Force applied to sewing springs",
        default=5,
        min=0.0,
        precision=4
    ) # type: ignore

    shrink: bpy.props.FloatProperty(
        name="Shrinking Factor",
        description="Factor to control the shrinking of the cloth",
        default=0,
        min=-1.0,
        max=1.0,
        precision=4
    ) # type: ignore
    collisions_label: bpy.props.StringProperty(
        name="",
        description="",
        default="Collisions",
        set=set_label
    )  # type: ignore

    collision_quality: bpy.props.IntProperty(
        name="Collision Quality",
        description="Accuracy of the simulation",
        default=4,
        min=1,
        max=20
    ) # type: ignore

    collision_distance: bpy.props.FloatProperty(
        name="Obj Distance",
        description="Distance at which cloth interacts with other objects",
        default=0.001,
        min=0.001,
        precision=4
    ) # type: ignore

    object_impulse_clamping: bpy.props.FloatProperty(
        name="Obj Imp Clamp",
        description="Clamp Collision Impulses",
        default=0.00,
        min=0.0,
        max=100.0,
        precision=4
    ) # type: ignore

    use_self_collision: bpy.props.BoolProperty(
        name="Enable Self Collision",
        description="Enable collisions between parts of the cloth itself",
        default=True
    ) # type: ignore

    self_collision_friction: bpy.props.FloatProperty(
        name="Friction",
        description="Distance at which cloth collides with itself",
        default=5,
        min=0.0,
        max=80.0,
        precision=4
    ) # type: ignore

    self_collision_distance: bpy.props.FloatProperty(
        name="Distance",
        description="Distance at which cloth collides with itself",
        default=0.001,
        min=0.0,
        precision=4
    ) # type: ignore

    self_impulse_clamping: bpy.props.FloatProperty(
        name="Impulse Clamping",
        description="Clamp Collision Impulses",
        default=0.00,
        min=0.0,
        max=100.0,
        precision=4
    )  # type: ignore

    field_label: bpy.props.StringProperty(
        name="",
        description="",
        default="Field Weights",
        set=set_label
    )  # type: ignore
    gravity: bpy.props.FloatProperty(
        name="Gravity",
        description="Strength of the gravity effect on the cloth",
        default=1,
        min=0.0,
        max=1.0,
        precision=4
    ) # type: ignore

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) != 0 and context.active_object.type == 'MESH'
    
    def execute(self, context):
        obj = context.active_object

        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Please select a mesh object.")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='VERT')

        check_verts = [v for v in obj.data.vertices if v.select]

        if len(check_verts) == 0:
            self.report({'ERROR'}, "No vertices selected for cloth sim.")
            return {'CANCELLED'}  


        bpy.ops.mesh.select_all(action='INVERT')
        bpy.ops.object.mode_set(mode='OBJECT')
        selected_verts = [v for v in obj.data.vertices if v.select]

        vg = obj.vertex_groups.get("QuickClothToolPinning")
       
        if vg:            
            obj.vertex_groups.remove(vg)
            vg = None

        vg = obj.vertex_groups.new(name="QuickClothToolPinning")     


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
    cloth.settings.quality = self.cloth_quality
    cloth.settings.time_scale = self.speed_multiplier
    cloth.settings.mass = self.cloth_mass
    cloth.settings.air_damping = self.air_viscosity

    
    cloth.settings.tension_stiffness = self.stension
    cloth.settings.compression_stiffness = self.scompression
    cloth.settings.shear_stiffness = self.sshear
    cloth.settings.bending_stiffness = self.sbending

    cloth.settings.tension_damping = self.dtension
    cloth.settings.compression_damping = self.dcompression
    cloth.settings.shear_damping = self.dshear
    cloth.settings.bending_damping = self.dbending

    cloth.settings.use_internal_springs = self.use_springs

    cloth.settings.use_pressure = self.use_pressure
    cloth.settings.uniform_pressure_force = self.pressure_force
   
    cloth.settings.vertex_group_mass = "QuickClothToolPinning"   
    cloth.settings.pin_stiffness = self.pinning_stiffness
    cloth.settings.use_sewing_springs = self.use_sewing
    cloth.settings.sewing_force_max = self.sewing_force
    cloth.settings.shrink_min = self.shrink

    cloth.collision_settings.collision_quality = self.collision_quality
    cloth.collision_settings.distance_min = self.collision_distance
    
    cloth.collision_settings.use_self_collision = self.use_self_collision
    cloth.collision_settings.self_friction = self.self_collision_friction
    cloth.collision_settings.self_distance_min = self.self_collision_distance
    cloth.collision_settings.self_impulse_clamp = self.self_impulse_clamping

    cloth.settings.effector_weights.gravity = self.gravity  
    return cloth.settings


class QUICKCLOTH_OT_quick_cloth_apply(bpy.types.Operator):
    """Applies a modifier named 'QuickCloth'."""
    bl_idname = "object.quick_cloth_apply"
    bl_label = "Apply QuickCloth Modifier"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        existing = [m for m in obj.modifiers if m.type == "CLOTH" and m.name == "QuickCloth"]
        return len(context.selected_objects) != 0 and context.active_object.type == 'MESH' and len(existing) == 1


    def execute(self, context):
        obj = context.active_object
        if obj:
            bpy.ops.object.mode_set(mode='OBJECT')   
            bpy.ops.object.modifier_apply(modifier="QuickCloth")        

            vg = obj.vertex_groups.get("QuickClothToolPinning")
            if vg:
                obj.vertex_groups.remove(vg)
            self.report({'INFO'}, "Applied 'QuickCloth' modifier.")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No object selected.")
            return {'CANCELLED'}
        

class QUICKCLOTH_OT_quick_cloth_weld(bpy.types.Operator):
    """Welds loose edges """
    bl_idname = "object.quick_cloth_weld"
    bl_label = "Weld Loose Edges"
    bl_options = {'REGISTER', 'UNDO'}


    distance: bpy.props.FloatProperty(
        name="Weld Distance",
        description="Distance for the weld modifier",
        default=.01,
        min=0.0,
        max=1.0,
        precision=4
    ) # type: ignore

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) != 0 and context.active_object.type == 'MESH'

    def execute(self, context):
        obj = context.active_object
        if obj:
            bpy.ops.object.mode_set(mode='OBJECT')   
            weld = obj.modifiers.new(name="QuickClothWeld", type='WELD')
            weld.mode = 'CONNECTED'
            weld.loose_edges = True
            weld.merge_threshold = self.distance
            bpy.ops.object.modifier_apply(modifier="QuickClothWeld")    
           
        return {'FINISHED'}



class QUICKCLOTH_OT_quick_cloth_remove(bpy.types.Operator):
    """Removes a modifier named 'QuickCloth'."""
    bl_idname = "object.quick_cloth_remove"
    bl_label = "Remove QuickCloth Modifier"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        existing = [m for m in obj.modifiers if m.type == "CLOTH" and m.name == "QuickCloth"]
        return len(context.selected_objects) != 0 and context.active_object.type == 'MESH' and len(existing) == 1

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


def register():
    bpy.utils.register_class(OBJECT_OT_add_quick_cloth_tool)
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_apply)
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_remove)
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_weld)

def unregister():
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_weld)
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_remove)
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_apply)
    bpy.utils.unregister_class(OBJECT_OT_add_quick_cloth_tool)
    