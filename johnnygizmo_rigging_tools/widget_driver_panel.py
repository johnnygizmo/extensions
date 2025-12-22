import bpy # type: ignore


class SHAPEKEY_MT_bone_collections(bpy.types.Menu):
    """Menu for selecting existing bone collections (Blender 4.0+)"""
    bl_label = "Bone Collections"
    bl_idname = "SHAPEKEY_MT_bone_collections"
    
    def draw(self, context):
        layout = self.layout
        armature = context.active_object
        
        if armature and hasattr(armature.data, 'collections'):
            for collection in armature.data.collections:
                op = layout.operator("shapekey.set_bone_collection", text=collection.name)
                op.collection_name = collection.name


class SHAPEKEY_MT_bone_groups(bpy.types.Menu):
    """Menu for selecting existing bone groups (Blender 3.x)"""
    bl_label = "Bone Groups"
    bl_idname = "SHAPEKEY_MT_bone_groups"
    
    def draw(self, context):
        layout = self.layout
        armature = context.active_object
        
        if armature and hasattr(armature.pose, 'bone_groups'):
            for group in armature.pose.bone_groups:
                op = layout.operator("shapekey.set_bone_collection", text=group.name)
                op.collection_name = group.name


class SHAPEKEY_OT_set_bone_collection(bpy.types.Operator):
    """Set the bone collection name"""
    bl_idname = "shapekey.set_bone_collection"
    bl_label = "Set Bone Collection"
    bl_options = {'INTERNAL'}
    
    collection_name: bpy.props.StringProperty() # type: ignore
    
    def execute(self, context):
        context.scene.shapekey_widget_settings.bone_collection_name = self.collection_name
        return {'FINISHED'}


class SHAPEKEY_PT_widget_panel(bpy.types.Panel):
    """ShapeKeyWidget Panel"""
    bl_label = "JohnnyGizmo ShapeKey Widget"
    bl_idname = "SHAPEKEY_PT_widget_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Rigging"
    
    @classmethod
    def poll(cls, context):
        if not context.active_object or context.active_object.type != 'ARMATURE':
            return False
        if context.mode != 'POSE':
            return False
        if not context.selected_pose_bones or len(context.selected_pose_bones) != 1:
            return False
        return True
    
    def draw(self, context):

        if not context.active_object or context.active_object.type != 'ARMATURE':
            
            layout = self.layout
            layout.label(text="Select an mesh and an armature in pose mode", icon='ERROR')
            return
        if context.mode != 'POSE':
            layout = self.layout
            layout.label(text="Select an mesh and an armature ", icon='ERROR')
            return
        if not context.selected_pose_bones or len(context.selected_pose_bones) != 1:
            layout = self.layout
            layout.label(text="Select an mesh and an armature", icon='ERROR')
            return


        
        layout = self.layout
        settings = context.scene.shapekey_widget_settings
        
        layout.label(text="Control Settings:")
        layout.prop(settings, "control_transform")
        layout.prop(settings, "control_axis")
        
        layout.separator()
        layout.label(text="Target:")
        layout.prop(settings, "target_mesh", icon='MESH_DATA')
        layout.prop(settings, "shape_key")
        
        
        # Display the current mix max of the selected shape key
        target_obj = settings.target_mesh 
                
        if target_obj and target_obj.type == 'MESH' and settings.shape_key in target_obj.data.shape_keys.key_blocks:                              
            
            shape_key_block = target_obj.data.shape_keys.key_blocks[settings.shape_key]                                  
            layout.label(text=f"Key Range: {shape_key_block.slider_min:.3f} to {shape_key_block.slider_max:.3f}")
        
        
        layout.separator()
        layout.label(text="Range Mapping:")
        col = layout.column(align=True)
        col.label(text="Bone Transform Range:")
        if settings.control_transform == 'ROTATION':
            col.prop(settings, "range_start_rot")
            col.prop(settings, "range_end_rot")
        else:
            col.prop(settings, "range_start")
            col.prop(settings, "range_end")
        
        col.separator()
        col.label(text="Shape Key Value Range:")
        col.prop(settings, "shapekey_value_min")
        col.prop(settings, "shapekey_value_max")
        
        layout.separator()
        layout.label(text="Constraints:")
        layout.prop(settings, "lock_to_axis")
        layout.prop(settings, "constrain_to_range")
        
        layout.separator()
        layout.label(text="Bone Collection:")
        
        # Show dropdown with existing collections if armature is selected
        if context.active_object and context.active_object.type == 'ARMATURE':
            armature = context.active_object
            row = layout.row(align=True)
            row.prop(settings, "bone_collection_name", text="")
            
            # Add a menu with existing collections
            if hasattr(armature.data, 'collections'):
                # Blender 4.0+ collections
                row.menu("SHAPEKEY_MT_bone_collections", text="", icon='DOWNARROW_HLT')
            else:
                # Blender 3.x bone groups
                row.menu("SHAPEKEY_MT_bone_groups", text="", icon='DOWNARROW_HLT')
        else:
            layout.prop(settings, "bone_collection_name")
        
        layout.separator()
        layout.operator("shapekey.create_widget_driver", text="Create Widget Driver", icon='DRIVER')


def register():
    bpy.utils.register_class(SHAPEKEY_MT_bone_collections)
    bpy.utils.register_class(SHAPEKEY_MT_bone_groups)
    bpy.utils.register_class(SHAPEKEY_OT_set_bone_collection)
    bpy.utils.register_class(SHAPEKEY_PT_widget_panel)


def unregister():
    bpy.utils.unregister_class(SHAPEKEY_PT_widget_panel)
    bpy.utils.unregister_class(SHAPEKEY_OT_set_bone_collection)
    bpy.utils.unregister_class(SHAPEKEY_MT_bone_groups)
    bpy.utils.unregister_class(SHAPEKEY_MT_bone_collections)
