import bpy # type: ignore
from bpy.props import StringProperty, EnumProperty, BoolProperty # type: ignore
from bpy.types import Operator # type: ignore

class JG_OT_bone_chain_rename(Operator):
    """Rename a chain of selected bones"""
    bl_idname = "jg.bone_chain_rename"
    bl_label = "Bone Chain Rename"
    bl_options = {'REGISTER', 'UNDO'}

    base_name: StringProperty(
        name="Name",
        description="Base name for the bones",
        default="Bone"
    )

    side: EnumProperty(
        name="Side",
        items=[
            ('L', 'Left (.L)', 'Left Side'),
            ('R', 'Right (.R)', 'Right Side'),
            ('Top', 'Top (.Top)', 'Top'),
            ('Bot', 'Bottom (.Bot)', 'Bottom'),
            ('Fr', 'Front (.Fr)', 'Front'),
            ('Bk', 'Back (.Bk)', 'Back'),
            ('NONE', 'None', 'No Side'),
        ],
        default='L'
    )

    bone_type: EnumProperty(
        name="Type",
        items=[
            ('DEF', 'Deform (DEF)', 'Deformation Bone'),
            ('CTRL', 'Control (CTRL)', 'Control Bone'),
            ('MCH', 'Mechanism (MCH)', 'Mechanism Bone'),
            ('NONE', 'None', 'No Type'),
        ],
        default='DEF'
    )

    rename_ik: BoolProperty(
        name="Rename IK Controllers & Poles",
        description="Rename associated IK constraints targets and poles if they exist",
        default=False
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        selected_bones = context.selected_bones
        if not selected_bones:
            selected_bones = context.selected_pose_bones

        if not selected_bones:
            self.report({'ERROR'}, "No bones selected")
            return {'CANCELLED'}

        # Sort bones by hierarchy depth (approximation: parent count or just linkage)
        # Detailed way: find the root most bone among selection.
        # Since we need to rename from "lowest" (meaning root-most in hierarchy tree, usually index 0 in a chain list if we walk down),
        # but the prompt says "Starting from the lowest bone in the chain", usually means Root -> Tip.
        # Let's verify "lowest" interpretation. "Lowest bone in the chain" might mean the one closest to the root (e.g. Shoulder) or the physical bottom?
        # Standard rigging naming convention usually counts 01 from Root to Tip (Shoulder -> Hand).
        # "Lowest bone in the chain" often refers to hierarchy root. I will assume Root -> Tip order.
        
        # Helper to calculate depth of a bone relative to the armature root
        def get_bone_depth(bone):
            depth = 0
            parent = bone.parent
            while parent:
                depth += 1
                parent = parent.parent
            return depth

        # Sort selected bones by depth
        # Note: In Edit Mode boundaries are EditBones, in Pose Mode they are PoseBones. Both have .parent checking.
        sorted_bones = sorted(selected_bones, key=get_bone_depth)
        
        # Validation: Check if it is a single connected chain?
        # The prompt says: "Check to make sure all selected bones are parents/children"
        # We can check if sorted_bones[i+1] is a direct child of sorted_bones[i].
        # However, a user might select a discontinuous chain. The prompt implies it's meant for a "set of bones selected... parents/children".
        # I will strictly enforce chain connectivity for now or warn. 
        # Actually, let's relax strict connectivity but warn if not linear. 
        # But for optimal numbering, they really should be connected.
        # Let's try to trace: sorted_bones[i+1].parent should be sorted_bones[i]. 
        # If not, it might be a broken chain or branching.
        
        is_chain_valid = True
        for i in range(len(sorted_bones) - 1):
            parent = sorted_bones[i]
            child = sorted_bones[i+1]
            if child.parent != parent:
                # It's possible there are intermediate bones not selected?
                # The prompt says "Check to make sure all selected bones are parents/children".
                # I'll enforce direct lineage for safety, or report warning.
                # Let's Report Error if not valid chain for now to stop bad renames.
                self.report({'ERROR'}, "Selected bones do not form a direct parent-child chain.")
                return {'CANCELLED'}

        # Process renaming
        for i, bone in enumerate(sorted_bones):
            number = f"{i+1:02d}"
            
            # Construct new name
            # {Type}_{Name}_{Number}.{Side}
            
            parts = []
            if self.bone_type != 'NONE':
                parts.append(self.bone_type)
            parts.append(self.base_name + number)
            # parts.append(number)
            
            new_name_base = "_".join(parts)
            
            suffix = ""
            if self.side != 'NONE':
                suffix = f".{self.side}"
                
            new_name = f"{new_name_base}{suffix}"
            
            old_name = bone.name
            bone.name = new_name
            
            # Handle IK if requested
            if self.rename_ik:
                # IK information is stored on PoseBones, even if we are in Edit Mode editing EditBones.
                # But to access constraints we need the PoseBone.
                # If we are in Edit Mode, we need to find the corresponding PoseBone.
                # Context object should be the armature.
                armature_ob = context.active_object
                pose_bone = armature_ob.pose.bones.get(new_name) # We just renamed it, so look up by new name
                
                if pose_bone:
                     for constraint in pose_bone.constraints:
                        if constraint.type == 'IK':
                            # Rename Target
                            if constraint.target:
                                if constraint.target.type == 'ARMATURE':
                                    subtarget_name = constraint.subtarget
                                    if subtarget_name:
                                        target_bone = armature_ob.pose.bones.get(subtarget_name)
                                        # Or maybe the target is in another object? 
                                        # Usually IK controllers are in the same rig or a control rig.
                                        # Prompt says: "Set the target bone name to {Name}_IK_CTRL.{SIDE}"
                                        
                                        # We need to find the bone that IS the target.
                                        # Beware: changing the name of the target bone might break the subtarget string reference if Blender doesn't update it auto-magically.
                                        # Blender usually handles renaming references well if done via API.
                                        
                                        # Wait, if the target bone is also selected, it might be renamed by the loop?
                                        # Usually IK target is NOT part of the chain (it's the controller).
                                        
                                        # Let's find the actual bone object for the target
                                        # Use the object from constraint.target (Object) and constraint.subtarget (Bone Name)
                                        
                                        target_ob = constraint.target
                                        target_bone_name = constraint.subtarget
                                        
                                        if target_ob and target_bone_name:
                                            # Rename target bone
                                            # We need to access the target bone in the target object
                                            if target_ob.type == 'ARMATURE':
                                                real_target_bone = target_ob.pose.bones.get(target_bone_name) # PoseBone
                                                # We need to rename the actual bone data/pose bone.
                                                # Renaming PoseBone.name renames the underlying Bone.
                                                
                                                if real_target_bone:

                                                    prefix = ""
                                                    if self.bone_type != 'NONE':
                                                        prefix = f"CTRL_"

                                                    ik_ctrl_name = f"{prefix}{self.base_name}_IK"
                                                    if self.side != 'NONE':
                                                        ik_ctrl_name += f".{self.side}"
                                                    
                                                    real_target_bone.name = ik_ctrl_name
                                                    # The constraint.subtarget should auto-update in Blender
                                else:
                                    self.report({'INFO'}, f"Non-Bone Target '{constraint.target.name}' was not Renamed")
                            
                            # Rename Pole Target
                            if constraint.pole_target:
                                if constraint.pole_target.type == 'ARMATURE':
                                    pole_subtarget_name = constraint.pole_subtarget
                                    if pole_subtarget_name:
                                        pole_ob = constraint.pole_target
                                        real_pole_bone = pole_ob.pose.bones.get(pole_subtarget_name)
                                        
                                        if real_pole_bone:
                                            prefix = ""
                                            if self.bone_type != 'NONE':
                                                prefix = f"CTRL_"
                                            
                                            pole_name = f"{prefix}{self.base_name}_IKPOLE"
                                            if self.side != 'NONE':
                                                pole_name += f".{self.side}"
                                            
                                            real_pole_bone.name = pole_name
                                else:
                                    self.report({'INFO'}, f"Non-Bone Pole Target '{constraint.pole_target.name}' was not Renamed")

        self.report({'INFO'}, f"Renamed {len(sorted_bones)} bones.")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(JG_OT_bone_chain_rename)

def unregister():
    bpy.utils.unregister_class(JG_OT_bone_chain_rename)
