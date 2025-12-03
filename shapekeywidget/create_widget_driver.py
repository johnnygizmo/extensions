import bpy  # type: ignore
from bpy.props import EnumProperty, FloatProperty, BoolProperty, PointerProperty, StringProperty  # type: ignore


def poll_mesh_objects(self, obj):
    """Poll function to filter only mesh objects"""
    return obj.type == 'MESH'


def get_shape_keys(self, context):
    """Get shape keys from the selected target mesh"""
    items = [('NONE', 'None', 'No shape key selected')]
    
    if self.target_mesh and self.target_mesh.data.shape_keys:
        for key in self.target_mesh.data.shape_keys.key_blocks:
            # Skip the basis shape key
            if key.name != 'Basis':
                items.append((key.name, key.name, f"Shape key: {key.name}"))
    
    return items


class SHAPEKEY_PG_widget_settings(bpy.types.PropertyGroup):
    """Property group to store widget driver settings"""
    
    # Transform type
    control_transform: EnumProperty(
        name="Control Transform",
        description="Type of transformation to use for control",
        items=[
            ('LOCATION', 'Location', 'Use location transform'),
            ('ROTATION', 'Rotation', 'Use rotation transform'),
            ('SCALE', 'Scale', 'Use scale transform'),
        ],
        default='LOCATION'
    ) # type: ignore
    
    # Axis of control
    control_axis: EnumProperty(
        name="Control Axis",
        description="Bone local axis to use for control",
        items=[
            ('X', 'X', 'X axis'),
            ('Y', 'Y', 'Y axis'),
            ('Z', 'Z', 'Z axis'),
        ],
        default='X'
    ) # type: ignore
    
    # Target mesh object
    target_mesh: PointerProperty(
        name="Target Mesh",
        description="Mesh object containing the shape keys",
        type=bpy.types.Object,
        poll=poll_mesh_objects
    ) # type: ignore
    
    # Shape key from target mesh
    shape_key: EnumProperty(
        name="Shape Key",
        description="Shape key to drive",
        items=get_shape_keys
    ) # type: ignore
    
    # Range start (for location and scale)
    range_start: FloatProperty(
        name="Range Start",
        description="Start of bone axis range (maps to shape key value 0)",
        default=0.0,
        soft_min=-10.0,
        soft_max=10.0
    ) # type: ignore
    
    # Range end (for location and scale)
    range_end: FloatProperty(
        name="Range End",
        description="End of bone axis range (maps to shape key value 1)",
        default=1.0,
        soft_min=-10.0,
        soft_max=10.0
    ) # type: ignore
    
    # Range start (for rotation in degrees)
    range_start_rot: FloatProperty(
        name="Range Start",
        description="Start of bone rotation range in degrees (maps to shape key value 0)",
        default=0.0,
        soft_min=-180.0,
        soft_max=180.0,
        subtype='ANGLE'
    ) # type: ignore
    
    # Range end (for rotation in degrees)
    range_end_rot: FloatProperty(
        name="Range End",
        description="End of bone rotation range in degrees (maps to shape key value 1)",
        default=90.0,
        soft_min=-180.0,
        soft_max=180.0,
        subtype='ANGLE'
    ) # type: ignore
    
    # Lock bone to axis
    lock_to_axis: BoolProperty(
        name="Lock to Axis",
        description="Lock the bone to only move along the selected axis",
        default=True
    ) # type: ignore
    
    # Constrain to range
    constrain_to_range: BoolProperty(
        name="Constrain to Range",
        description="Constrain the bone movement to the target range",
        default=True
    ) # type: ignore
    
    # Bone collection/group name
    bone_collection_name: StringProperty(
        name="Bone Collection",
        description="Name of the bone collection/group to assign the bone to",
        default="CTL"
    ) # type: ignore
    
    # Shape key value range start
    shapekey_value_min: FloatProperty(
        name="Shape Key Min",
        description="Minimum shape key value to map to",
        default=0.0,
        soft_min=-1.0,
        soft_max=1.0
    ) # type: ignore
    
    # Shape key value range end
    shapekey_value_max: FloatProperty(
        name="Shape Key Max",
        description="Maximum shape key value to map to",
        default=1.0,
        soft_min=-1.0,
        soft_max=1.0
    ) # type: ignore


class SHAPEKEY_OT_create_widget_driver(bpy.types.Operator):
    """Create a shape key driver controlled by bone movement"""
    bl_idname = "shapekey.create_widget_driver"
    bl_label = "Create Widget Driver"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        settings = context.scene.shapekey_widget_settings
        
        # Validate inputs
        if not settings.target_mesh:
            self.report({'ERROR'}, "No target mesh selected")
            return {'CANCELLED'}
        
        # Get target mesh object
        target_obj = settings.target_mesh
        if target_obj.type != 'MESH':
            self.report({'ERROR'}, "Selected object is not a mesh")
            return {'CANCELLED'}
        
        if settings.shape_key == 'NONE':
            self.report({'ERROR'}, "No shape key selected")
            return {'CANCELLED'}
        
        # Get the selected bone
        armature = context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "No armature selected")
            return {'CANCELLED'}
        
        if not context.selected_pose_bones:
            self.report({'ERROR'}, "No bone selected")
            return {'CANCELLED'}
        
        bone = context.selected_pose_bones[0]
        
        # Get target mesh and shape key
        if not target_obj.data.shape_keys:
            self.report({'ERROR'}, "Target mesh has no shape keys")
            return {'CANCELLED'}
        
        shape_key_block = target_obj.data.shape_keys.key_blocks.get(settings.shape_key)
        if not shape_key_block:
            self.report({'ERROR'}, f"Shape key '{settings.shape_key}' not found")
            return {'CANCELLED'}
        
        # Update shape key slider range if necessary
        # Expand slider_min if our minimum is lower
        if settings.shapekey_value_min < shape_key_block.slider_min:
            shape_key_block.slider_min = settings.shapekey_value_min
        
        # Expand slider_max if our maximum is higher
        if settings.shapekey_value_max > shape_key_block.slider_max:
            shape_key_block.slider_max = settings.shapekey_value_max
        
        # Rename the bone
        new_bone_name = f"{target_obj.name}.{settings.shape_key}_CTL"
        bone.name = new_bone_name
        
        # Create or get the bone group/collection and assign the bone to it
        collection_name = settings.bone_collection_name if settings.bone_collection_name else "CTL"
        
        # In Blender 4.0+, bone groups are called bone collections
        if hasattr(armature.data, 'collections'):
            # Blender 4.0+ uses bone collections
            target_collection = None
            for collection in armature.data.collections:
                if collection.name == collection_name:
                    target_collection = collection
                    break
            
            if not target_collection:
                target_collection = armature.data.collections.new(name=collection_name)
            
            # Remove bone from all collections first
            for collection in armature.data.collections:
                if bone.bone.name in [b.name for b in collection.bones]:
                    collection.unassign(bone)
            
            # Add bone to target collection
            target_collection.assign(bone)
        else:
            # Blender 3.x and earlier uses bone groups
            target_group = None
            for group in armature.pose.bone_groups:
                if group.name == collection_name:
                    target_group = group
                    break
            
            if not target_group:
                target_group = armature.pose.bone_groups.new(name=collection_name)
            
            bone.bone_group = target_group
        
        # Clear existing transformation locks on the bone
        bone.lock_location = [False, False, False]
        bone.lock_rotation = [False, False, False]
        bone.lock_rotation_w = False
        bone.lock_scale = [False, False, False]
        
        # Remove existing limit constraints that match the selected mode
        constraint_type_map = {
            'LOCATION': 'LIMIT_LOCATION',
            'ROTATION': 'LIMIT_ROTATION',
            'SCALE': 'LIMIT_SCALE'
        }
        constraint_type = constraint_type_map[settings.control_transform]
        
        # Remove matching constraints
        for constraint in list(bone.constraints):
            if constraint.type == constraint_type:
                bone.constraints.remove(constraint)
        
        # Remove existing driver on the shape key value if present
        try:
            shape_key_block.driver_remove("value")
        except Exception:
            pass  # No driver to remove
        
        # Create new driver
        fcurve = shape_key_block.driver_add("value")
        driver = fcurve.driver
        driver.type = 'SCRIPTED'
        
        # Add variable for bone transform
        var = driver.variables.new()
        var.name = "bone_transform"
        var.type = 'TRANSFORMS'
        
        # Set up the variable target
        target = var.targets[0]
        target.id = armature
        target.bone_target = bone.name
        
        # Set transform type based on selection
        transform_prefix = {'LOCATION': 'LOC', 'ROTATION': 'ROT', 'SCALE': 'SCALE'}[settings.control_transform]
        target.transform_type = f'{transform_prefix}_{settings.control_axis}'
        target.transform_space = 'LOCAL_SPACE'
        
        # Create the driver expression to map bone transform range to shape key value range
        # Formula: ((value - bone_start) / (bone_end - bone_start)) * (sk_max - sk_min) + sk_min
        # Use appropriate range properties based on transform type
        if settings.control_transform == 'ROTATION':
            range_start = settings.range_start_rot
            range_end = settings.range_end_rot
        else:
            range_start = settings.range_start
            range_end = settings.range_end
            
        range_size = range_end - range_start
        if abs(range_size) < 0.0001:
            self.report({'ERROR'}, "Range start and end cannot be the same")
            return {'CANCELLED'}
        
        # Get shape key value range
        sk_min = settings.shapekey_value_min
        sk_max = settings.shapekey_value_max
        sk_range = sk_max - sk_min
        
        # Build expression: normalized value (0-1) mapped to shape key range
        normalized = f"(bone_transform - ({range_start})) / ({range_size})"
        clamped = f"max(0, min(1, {normalized}))"
        mapped = f"{clamped} * ({sk_range}) + ({sk_min})"
        
        driver.expression = mapped
        
        # Apply constraints if requested
        if settings.lock_to_axis:
            # Lock other axes based on transform type
            lock_map = {
                'X': [False, True, True],
                'Y': [True, False, True],
                'Z': [True, True, False]
            }
            lock_x, lock_y, lock_z = lock_map[settings.control_axis]
            
            if settings.control_transform == 'LOCATION':
                # Lock all rotation and scale, and other location axes
                bone.lock_location[0] = lock_x
                bone.lock_location[1] = lock_y
                bone.lock_location[2] = lock_z
                bone.lock_rotation = [True, True, True]
                bone.lock_rotation_w = True
                bone.lock_scale = [True, True, True]
            elif settings.control_transform == 'ROTATION':
                # Lock all location and scale, and other rotation axes
                bone.lock_location = [True, True, True]
                bone.lock_rotation[0] = lock_x
                bone.lock_rotation[1] = lock_y
                bone.lock_rotation[2] = lock_z
                bone.lock_scale = [True, True, True]
            else:  # SCALE
                # Lock all location and rotation, and other scale axes
                bone.lock_location = [True, True, True]
                bone.lock_rotation = [True, True, True]
                bone.lock_rotation_w = True
                bone.lock_scale[0] = lock_x
                bone.lock_scale[1] = lock_y
                bone.lock_scale[2] = lock_z
        
        if settings.constrain_to_range:
            # Use appropriate range properties based on transform type
            if settings.control_transform == 'ROTATION':
                range_start = settings.range_start_rot
                range_end = settings.range_end_rot
            else:
                range_start = settings.range_start
                range_end = settings.range_end
                
            # Add appropriate limit constraint based on transform type
            if settings.control_transform == 'LOCATION':
                constraint = bone.constraints.new('LIMIT_LOCATION')
                constraint.name = f"ShapeKey_{settings.shape_key}_Limit"
                constraint.use_transform_limit = True
                constraint.owner_space = 'LOCAL'
                
                axis_idx = {'X': 0, 'Y': 1, 'Z': 2}[settings.control_axis]
                if axis_idx == 0:
                    constraint.use_min_x = True
                    constraint.use_max_x = True
                    constraint.min_x = range_start
                    constraint.max_x = range_end
                elif axis_idx == 1:
                    constraint.use_min_y = True
                    constraint.use_max_y = True
                    constraint.min_y = range_start
                    constraint.max_y = range_end
                else:
                    constraint.use_min_z = True
                    constraint.use_max_z = True
                    constraint.min_z = range_start
                    constraint.max_z = range_end
                    
            elif settings.control_transform == 'ROTATION':
                constraint = bone.constraints.new('LIMIT_ROTATION')
                constraint.name = f"ShapeKey_{settings.shape_key}_Limit"
                constraint.use_transform_limit = True
                constraint.owner_space = 'LOCAL'
                
                axis_idx = {'X': 0, 'Y': 1, 'Z': 2}[settings.control_axis]
                if axis_idx == 0:
                    constraint.use_limit_x = True
                    constraint.min_x = range_start
                    constraint.max_x = range_end
                elif axis_idx == 1:
                    constraint.use_limit_y = True
                    constraint.min_y = range_start
                    constraint.max_y = range_end
                else:
                    constraint.use_limit_z = True
                    constraint.min_z = range_start
                    constraint.max_z = range_end
                    
            else:  # SCALE
                constraint = bone.constraints.new('LIMIT_SCALE')
                constraint.name = f"ShapeKey_{settings.shape_key}_Limit"
                constraint.use_transform_limit = True
                constraint.owner_space = 'LOCAL'
                
                axis_idx = {'X': 0, 'Y': 1, 'Z': 2}[settings.control_axis]
                if axis_idx == 0:
                    constraint.use_min_x = True
                    constraint.use_max_x = True
                    constraint.min_x = range_start
                    constraint.max_x = range_end
                elif axis_idx == 1:
                    constraint.use_min_y = True
                    constraint.use_max_y = True
                    constraint.min_y = range_start
                    constraint.max_y = range_end
                else:
                    constraint.use_min_z = True
                    constraint.use_max_z = True
                    constraint.min_z = range_start
                    constraint.max_z = range_end
        
        self.report({'INFO'}, f"Driver created: {bone.name} ({settings.control_transform} {settings.control_axis}) -> {settings.shape_key}")
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SHAPEKEY_PG_widget_settings)
    bpy.utils.register_class(SHAPEKEY_OT_create_widget_driver)
    bpy.types.Scene.shapekey_widget_settings = bpy.props.PointerProperty(type=SHAPEKEY_PG_widget_settings)


def unregister():
    del bpy.types.Scene.shapekey_widget_settings
    bpy.utils.unregister_class(SHAPEKEY_OT_create_widget_driver)
    bpy.utils.unregister_class(SHAPEKEY_PG_widget_settings)
