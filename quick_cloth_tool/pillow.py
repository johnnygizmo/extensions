
import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import FloatProperty, IntProperty, BoolProperty
#from bpy import context


def update_cloth_settings(self,context):
    ob = bpy.context.active_object


    vg = ob.vertex_groups.get("QuickPillowPinning")
       
    if vg:            
        ob.vertex_groups.remove(vg)
        vg = None

    vg = ob.vertex_groups.new(name="QuickPillowPinning")        
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')
    selected_verts = [v for v in ob.data.vertices if v.select]

    if not selected_verts:
        ob.vertex_groups.remove(vg)
        vg = None
    else:
        for v in selected_verts:
            vg.add([v.index], 1.0, 'REPLACE')

    if ob.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    pillow_mod = None
    existing = [m for m in ob.modifiers if m.type == "CLOTH"]
    if len(existing) == 0:
        pillow_mod = ob.modifiers.new(name="QuickPillow", type='CLOTH')
        bpy.ops.object.modifier_move_to_index(modifier="QuickPillow",index=0)
    else:
        pillow_mod = existing[0]
        existing[0].name = "QuickPillow"
    pillow_mod.settings.use_pressure = True
    pillow_mod.settings.pin_stiffness = self.pin_stiff
    pillow_mod.settings.uniform_pressure_force = self.pressure
    pillow_mod.collision_settings.use_self_collision = self.selfcol 
    pillow_mod.collision_settings.self_distance_min = self.selfdist
    pillow_mod.settings.effector_weights.gravity = self.gravity
    pillow_mod.settings.quality = self.quality
    pillow_mod.collision_settings.collision_quality = self.cquality
    pillow_mod.collision_settings.distance_min = self.coldist
    pillow_mod.collision_settings.use_collision = self.col
    pillow_mod.settings.use_sewing_springs = self.use_sewing
    pillow_mod.settings.sewing_force_max = self.sewing_force

    if vg != None:
        pillow_mod.settings.vertex_group_mass = "QuickPillowPinning"

    if 'Subdivision' not in ob.modifiers:
        bpy.ops.object.modifier_add(type='SUBSURF')
    ob.modifiers['Subdivision'].levels = self.sublevels
    ob.modifiers['Subdivision'].render_levels = self.sublevels

class OBJECT_OT_add_quick_pillow(bpy.types.Operator):
    """Quick Pillow"""
    bl_idname = "object.add_quick_pillow"
    bl_label = "Quick Pillow"
    bl_options = {'REGISTER', 'UNDO'}

    pressure: FloatProperty(
        name="Pressure",
        default=1.0
    )
    quality: IntProperty(
        name="Quality",
        default=5
    )
    gravity: FloatProperty(
        name="Gravity",
        default=0.0
    )
    col: BoolProperty(
        name="Collisions",
        default=True
    )    
    cquality: IntProperty(
        name="Coll. Quality",
        default=2
    )    
    coldist: FloatProperty(
        name="Coll Dist",
        default=.01
    )    
    selfcol: BoolProperty(
        name="Self Collisions",
        default=False
    )
    selfdist: FloatProperty(
        name="Self Coll Dist",
        default=.01
    )

    sublevels: IntProperty(
        name="Subdiv Levels",
        default=2
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
    pin_stiff: bpy.props.FloatProperty(
        name="Pinning Stiffness",
        description="Stiffness of the pinning group",
        default=1,
        min=0.0,
        max=100.0,
        precision=4
    )

    def execute(self, context):
        update_cloth_settings(self,context)
        return {'FINISHED'}



class OBJECT_OT_apply_quick_pillow(bpy.types.Operator):
    """Applies a modifier named 'QuickCloth'."""
    bl_idname = "object.apply_quick_pillow"
    bl_label = "Apply QuickPillow Modifier"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if obj:
            bpy.ops.object.mode_set(mode='OBJECT')   

            bpy.ops.object.modifier_apply(modifier="QuickPillow")
            
            vg = obj.vertex_groups.get("QuickPillowPinning")
            if vg:
                obj.vertex_groups.remove(vg)
            self.report({'INFO'}, "Applied 'QuickCloth' modifier.")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No object selected.")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(OBJECT_OT_add_quick_pillow)
    bpy.utils.register_class(OBJECT_OT_apply_quick_pillow)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_quick_pillow)
    bpy.utils.unregister_class(OBJECT_OT_apply_quick_pillow)
    
