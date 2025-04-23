import bpy

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
    )


    speed_multiplier: bpy.props.FloatProperty(
        name="Speed Multiplier",
        description="Multiplier for the speed of the cloth simulation",
        default=1,
        min=0.0,
        precision=4
    )

    cloth_mass: bpy.props.FloatProperty(
        name="Vertex Mass",
        description="Mass of the cloth vertices",
        default=3.0,
        min=0.01,
        soft_max=10.0
    )
    air_viscosity: bpy.props.FloatProperty(
        name="Air Viscosity",
        description="Air Viscosity",
        default=1.0,
        min=0.00,
        soft_max=10.0
    )

    stiffness: bpy.props.StringProperty(
        name="",
        description="",
        default="Stiffness",
        set=set_label
    ) 



    stension: bpy.props.FloatProperty(
        name="Tension",
        description="Tension",
        default=15.0,
        min=0.00
    )
    scompression: bpy.props.FloatProperty(
        name="Compression",
        description="Comspression",
        default=15.0,
        min=0.00
    )
    sshear: bpy.props.FloatProperty(
        name="Shear",
        description="Shear",
        default=5.0,
        min=0.00
    )

    sbending: bpy.props.FloatProperty(
        name="Bending",
        description="Bending",
        default=1.0,
        min=0.00
    )
    damping: bpy.props.StringProperty(
        name="",
        description="",
        default="Damping",
        set=set_label
    ) 
    dtension: bpy.props.FloatProperty(
        name="Tension",
        description="Tension",
        default=15.0,
        min=0.00
    )
    dcompression: bpy.props.FloatProperty(
        name="Compression",
        description="Comspression",
        default=15.0,
        min=0.00
    )
    dshear: bpy.props.FloatProperty(
        name="Shear",
        description="Shear",
        default=5.0,
        min=0.00
    )
    dbending: bpy.props.FloatProperty(
        name="Bending",
        description="Bending",
        default=1.0,
        min=0.00
    )
    springs_label: bpy.props.StringProperty(
        name="",
        description="",
        default="Internal Springs",
        set=set_label
    ) 
    use_springs: bpy.props.BoolProperty(
        name="Enable Springs",
        description="Enable internal volume structure",
        default=False
    )
    pressure_label: bpy.props.StringProperty(
        name="",
        description="",
        default="Pressure",
        set=set_label
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
    shape_label: bpy.props.StringProperty(
        name="",
        description="",
        default="Shape",
        set=set_label
    ) 
    pinning_stiffness: bpy.props.FloatProperty(
        name="Pinning Stiffness",
        description="Pin Spring Stiffness",
        default=1,
        min=0.0,
        precision=4,
        max=50
    )        
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

    shrink: bpy.props.FloatProperty(
        name="Shrinking Factor",
        description="Factor to control the shrinking of the cloth",
        default=0,
        min=-1.0,
        max=1.0,
        precision=4
    )
    collisions_label: bpy.props.StringProperty(
        name="",
        description="",
        default="Collisions",
        set=set_label
    ) 

    collision_quality: bpy.props.IntProperty(
        name="Collision Quality",
        description="Accuracy of the simulation",
        default=4,
        min=1,
        max=20
    )

    collision_distance: bpy.props.FloatProperty(
        name="Obj Distance",
        description="Distance at which cloth interacts with other objects",
        default=0.001,
        min=0.0,
        precision=4
    )

    object_impulse_clamping: bpy.props.FloatProperty(
        name="Obj Imp Clamp",
        description="Clamp Collision Impulses",
        default=0.00,
        min=0.0,
        max=100.0,
        precision=4
    )

    use_self_collision: bpy.props.BoolProperty(
        name="Enable Self Collision",
        description="Enable collisions between parts of the cloth itself",
        default=True
    )

    self_collision_friction: bpy.props.FloatProperty(
        name="Friction",
        description="Distance at which cloth collides with itself",
        default=5,
        min=0.0,
        max=80.0,
        precision=4
    )

    self_collision_distance: bpy.props.FloatProperty(
        name="Distance",
        description="Distance at which cloth collides with itself",
        default=0.001,
        min=0.0,
        precision=4
    )

    self_impulse_clamping: bpy.props.FloatProperty(
        name="Impulse Clamping",
        description="Clamp Collision Impulses",
        default=0.00,
        min=0.0,
        max=100.0,
        precision=4
    ) 

    field_label: bpy.props.StringProperty(
        name="",
        description="",
        default="Field Weights",
        set=set_label
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




class QUICKCLOTH_OT_quick_cloth_stitch_vertring(bpy.types.Operator):
    """Applies a modifier named 'QuickCloth'."""
    bl_idname = "object.quick_cloth_stitch_vertring"
    bl_label = "Add Stiching Inside a Vertex Ring"
    bl_options = {'REGISTER', 'UNDO'}
    
    vertSkip: bpy.props.IntProperty(
        name="Vertices to Skip",
        description="Amount of vertices to skip when stitching",
        min=1,
        default=3
    )

    offset: bpy.props.IntProperty(
        name="Vertex Offset",
        description="Offset for the stitching",
        min=0,
        default=0
    )

    extrudeControl: bpy.props.BoolProperty(
        name="Extrude Control Ring",
        description="Extrude the control ring",
        default=True
    )

    extrudeControlDistance: bpy.props.FloatProperty(
        name="Extrude Control Ring Distance",
        description="Distance to extrude the control ring",
        default=.2
    )

    def execute(self, context):
        obj = context.active_object
        if obj:
            bpy.ops.object.mode_set(mode='EDIT')   
            bpy.ops.mesh.select_nth(skip=self.vertSkip, offset=self.offset)
            bpy.ops.mesh.edge_face_add()     
            if self.extrudeControl:
                bpy.ops.mesh.extrude_region_shrink_fatten(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_shrink_fatten={"value":self.extrudeControlDistance, "use_even_offset":False, "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":0.385543, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "release_confirm":True, "use_accurate":False})
                bpy.ops.mesh.select_more()  
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
    
    damping: bpy.props.FloatProperty(
        name="Damping",
        description="Damping",
        default=.1,
        min=0.0,
        max=1.0,
        precision=4
    )
    thickness_outer: bpy.props.FloatProperty(
        name="Thickness Outer",
        description="Outer Face Thickness",
        default=.02,
        min=0.001,
        max=1.0,
        precision=4
    ) 
    friction: bpy.props.FloatProperty(
        name="Friction",
        description="friction",
        default=5,
        min=0.0,
        max=80.0,
        precision=4
    )
    single: bpy.props.BoolProperty(
        name="Single Sided",
        description="Cloth Acts with Collision Normals",
        default=True
    )
    override: bpy.props.BoolProperty(
        name="Override Normals",
        description="Cloth Impulses Act with Collision Normals",
        default=False
    )


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


def register():
    bpy.utils.register_class(OBJECT_OT_add_quick_cloth_tool)
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_apply)
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_remove)
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_stitch_edgeloops)
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_add_collision)
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_stitch_vertring)

def unregister():
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_stitch_vertring)
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_add_collision)
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_stitch_edgeloops)
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_remove)
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_apply)
    bpy.utils.unregister_class(OBJECT_OT_add_quick_cloth_tool)
    