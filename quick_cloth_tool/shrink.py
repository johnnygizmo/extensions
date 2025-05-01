import bpy # type: ignore

class QUICKCLOTH_OT_quick_cloth_add_shrink(bpy.types.Operator):
    """Add Shrink Modifier"""
    bl_idname = "object.quick_cloth_add_shrink"
    bl_label = "Add Shrink Modifier"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) != 0 and context.active_object.type == 'MESH' 
    

    # damping: bpy.props.FloatProperty(
    #     name="Damping",
    #     description="Damping",
    #     default=.1,
    #     min=0.0,
    #     max= 1,
    # ) 
    # friction: bpy.props.FloatProperty(
    #     name="Friction",
    #     description="Friction",
    #     default=5,
    #     min=0.0,
    #     max= 80.0,
    # ) 
    offset: bpy.props.FloatProperty(
        name="Offset",
        description="Offset",
        default=0.0
    )  # type: ignore

    method: bpy.props.EnumProperty(
        name="Method",
        description="Method",
        items=[
            ('NEAREST_SURFACEPOINT', "Nearest Surface Point", "Shrink the mesh to the nearest target surface."),
            ('TARGET_PROJECT', "Target Normal", "Shrink the mesh to the nearest target surface along the interpolated vertex normals of the target."),
            ('NEAREST_VERTEX', "Nearest Vertex", "Shrink the mesh to the nearest target vertex."),
        ],
        default='NEAREST_SURFACEPOINT'
    ) # type: ignore
    
    # single: bpy.props.BoolProperty(
    #     name="Single Sided",
    #     description="Single Sided",
    #     default=True
    # ) 
    # override:bpy.props.BoolProperty(
    #     name="Override Normals",
    #     description="Override Normals",
    #     default=False
    # ) 

    def execute(self, context):

        if len(context.selected_objects) != 2:
            self.report({'ERROR'}, "Select two objects to add a shrink modifier.")
            return {'CANCELLED'}
        
        obj = context.active_object
        target = context.selected_objects[1] if context.selected_objects[0] == obj else context.selected_objects[0]

        if obj and target:
            selected_verts = [v for v in obj.data.vertices if v.select]

            if len(selected_verts) == 0:
                self.report({'ERROR'}, "No vertices selected for shrink.")
                return {'CANCELLED'}


            bpy.ops.object.mode_set(mode='OBJECT')

            vg = obj.vertex_groups.get("QuickClothToolShrink")
        
            if vg:            
                obj.vertex_groups.remove(vg)
                vg = None

            vg = obj.vertex_groups.new(name="QuickClothToolShrink")                 

            for v in selected_verts:
                vg.add([v.index], 1.0, 'REPLACE')

            existing = [m for m in obj.modifiers if m.type == "SHRINKWRAP"]
            if len(existing) == 1:
                bpy.ops.object.modifier_remove(modifier=existing[0].name)
        
            shrink = obj.modifiers.new(name="QuickClothShrink", type='SHRINKWRAP')
            shrink.target = target
            shrink.wrap_method = self.method
            shrink.wrap_mode = 'ABOVE_SURFACE'
            shrink.use_negative_direction = True
            shrink.use_project_x = True
            shrink.use_project_y = True
            shrink.use_project_z = True
            shrink.offset = self.offset
            shrink.vertex_group = "QuickClothToolShrink"

            bpy.ops.object.modifier_move_to_index(modifier="QuickClothShrink",index=0)    
            return {'FINISHED'}
    
class QUICKCLOTH_OT_quick_cloth_apply_shrink(bpy.types.Operator):
    """Apply Shrink Modifier"""
    bl_idname = "object.quick_cloth_apply_shrink"
    bl_label = "Apply Shrink Modifier"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if obj == None or obj.type != 'MESH':
            return False
        existing = [m for m in obj.modifiers if m.type == "SHRINKWRAP" and m.name == "QuickClothShrink"]
        return len(context.selected_objects) != 0 and context.active_object.type == 'MESH' and len(existing) == 1
    
    def execute(self, context):
        obj = context.active_object
        if obj:
            bpy.ops.object.mode_set(mode='OBJECT')   
            bpy.ops.object.modifier_apply(modifier="QuickClothShrink")
         

            vg = obj.vertex_groups.get("QuickClothToolShrink")
            if vg:
                obj.vertex_groups.remove(vg)
            self.report({'INFO'}, "Applied 'QuickCloth Shrink' modifier.")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No object selected.")
            return {'CANCELLED'}     


class QUICKCLOTH_OT_quick_cloth_rem_shrink(bpy.types.Operator):
    """Remove Shrink Modifier"""

    bl_idname = "object.quick_cloth_rem_shrink"
    bl_label = "Remove Shrink Modifier"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if obj == None or obj.type != 'MESH':
            return False
        existing = [m for m in obj.modifiers if m.type == "SHRINKWRAP" and m.name == "QuickClothShrink"]
        return len(context.selected_objects) != 0 and context.active_object.type == 'MESH' and len(existing) == 1
    
    def execute(self, context):
        obj = context.active_object
        if obj:
            bpy.ops.object.mode_set(mode='OBJECT')   
            existing = [m for m in obj.modifiers if m.type == "SHRINKWRAP" and m.name == "QuickClothShrink"]
            if len(existing) == 1:
                bpy.ops.object.modifier_remove(modifier=existing[0].name)
        
            vg = obj.vertex_groups.get("QuickClothToolShrink")
            if vg:
                obj.vertex_groups.remove(vg)
            self.report({'INFO'}, "Removed 'QuickCloth Shrink' modifier.")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No object selected.")
            return {'CANCELLED'}

def register():
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_add_shrink)
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_apply_shrink)
    bpy.utils.register_class(QUICKCLOTH_OT_quick_cloth_rem_shrink)
    

def unregister():
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_rem_shrink)
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_apply_shrink)
    bpy.utils.unregister_class(QUICKCLOTH_OT_quick_cloth_add_shrink)