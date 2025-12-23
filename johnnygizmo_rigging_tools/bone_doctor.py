import bpy
from bpy.props import BoolProperty

class ARMATURE_OT_bone_doctor(bpy.types.Operator):
    """Bone Doctor: Perform various cleanup tasks on the armature"""
    bl_idname = "armature.bone_doctor"
    bl_label = "Bone Doctor"
    bl_options = {'REGISTER', 'UNDO'}

    disable_deform_on_ik_targets: BoolProperty(
        name="Disable Deform on IK Targets",
        description="Uncheck 'use_deform' for bones that are targets of IK constraints",
        default=True
    )

    disable_deform_on_non_def: BoolProperty(
        name="Disable Deform on Non-DEF Bones",
        description="Uncheck 'use_deform' for bones that do not start with 'DEF_'",
        default=True
    )

    enable_deform_on_def: BoolProperty(
        name="Enable Deform on DEF Bones",
        description="Check 'use_deform' for bones that start with 'DEF_'",
        default=True
    )

    move_def_to_collection: BoolProperty(
        name="Move DEF Bones to Collection",
        description="Move bones starting with 'DEF_' to a 'DEF' bone collection",
        default=True
    )

    move_mch_to_collection: BoolProperty(
        name="Move MCH Bones to Collection",
        description="Move bones starting with 'MCH_' to a 'MCH' bone collection",
        default=True
    )

    move_ctrl_to_collection: BoolProperty(
        name="Move CTRL Bones to Collection",
        description="Move bones starting with 'CTRL_' to a 'CTRL' bone collection",
        default=True
    )

    clean_symmetry_names: BoolProperty(
        name="Clean Symmetry Naming",
        description="Standardize symmetry suffixes to use periods with proper capitalization (.L, .R, .Top, .Bot, .Fr, .Bk)",
        default=True
    )

    apply_armature_transforms: BoolProperty(
        name="Apply Armature Transforms",
        description="Apply armature object transforms if scale ≠ (1,1,1) or rotation ≠ (0,0,0)",
        default=True
    )

    generate_report: BoolProperty(
        name="Generate Report",
        description="Create a text datablock with warnings about potential rigging issues",
        default=True
    )

    @classmethod
    def poll(cls, context):
        return (context.active_object and context.active_object.type == 'ARMATURE')

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "disable_deform_on_ik_targets")
        layout.prop(self, "disable_deform_on_non_def")
        layout.prop(self, "enable_deform_on_def")
        
        # Collection assignment in a row
        row = layout.row()
        row.label(text="Move Bones to Groups")
        row.prop(self, "move_def_to_collection", text="DEF")
        row.prop(self, "move_mch_to_collection", text="MCH")
        row.prop(self, "move_ctrl_to_collection", text="CTRL")
        
        layout.prop(self, "clean_symmetry_names")
        layout.prop(self, "apply_armature_transforms")
        layout.prop(self, "generate_report")

    def execute(self, context):
        import re
        
        arm_obj = context.active_object
        arm_data = arm_obj.data

        # Task: Apply armature transforms if needed
        if self.apply_armature_transforms:
            # Check if scale is not (1,1,1) or rotation is not (0,0,0)
            needs_apply = False
            
            # Check scale
            if not all(abs(s - 1.0) < 0.0001 for s in arm_obj.scale):
                needs_apply = True
            
            # Check rotation (Euler)
            if not all(abs(r) < 0.0001 for r in arm_obj.rotation_euler):
                needs_apply = True
            
            if needs_apply:
                # Store current mode
                original_mode = arm_obj.mode
                
                # Switch to object mode to apply transforms
                if original_mode != 'OBJECT':
                    bpy.ops.object.mode_set(mode='OBJECT')
                
                # Apply transforms
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
                # Restore original mode
                if original_mode != 'OBJECT':
                    bpy.ops.object.mode_set(mode=original_mode)

        # 1. Identify IK Targets
        ik_targets = set()
        for bone in arm_obj.pose.bones:
            for constraint in bone.constraints:
                if constraint.type == 'IK':
                    if constraint.target == arm_obj and constraint.subtarget:
                        ik_targets.add(constraint.subtarget)

        # Switch to Edit Mode for some operations if needed, but properties like use_deform 
        # are accessible in Object/Pose mode on the data.bones
        # Collections are also on data.collections
        
        # We can do everything in Object/Pose mode by accessing arm_data.bones

        # Ensure collections exist if needed
        def_collection = None
        mch_collection = None
        ctrl_collection = None
        
        if self.move_def_to_collection:
            def_collection = arm_data.collections.get("DEF")
            if not def_collection:
                def_collection = arm_data.collections.new("DEF")
        
        if self.move_mch_to_collection:
            mch_collection = arm_data.collections.get("MCH")
            if not mch_collection:
                mch_collection = arm_data.collections.new("MCH")
        
        if self.move_ctrl_to_collection:
            ctrl_collection = arm_data.collections.get("CTRL")
            if not ctrl_collection:
                ctrl_collection = arm_data.collections.new("CTRL")
            
        for bone in arm_data.bones:
            # Task: IK Targets have use_deform unchecked
            if self.disable_deform_on_ik_targets:
                if bone.name in ik_targets:
                    bone.use_deform = False

            # Task: Bones that do not start with DEF_ have use_deform unchecked
            if self.disable_deform_on_non_def:
                if not bone.name.startswith("DEF_"):
                    bone.use_deform = False

            # Task: Bones that start DEF_ have use_deform checked
            if self.enable_deform_on_def:
                if bone.name.startswith("DEF_"):
                    bone.use_deform = True

            # Task: Move DEF bones to 'DEF' collection
            if self.move_def_to_collection and bone.name.startswith("DEF_"):
                # Assign to DEF collection
                def_collection.assign(bone)
                
                # Remove from all other collections
                for col in arm_data.collections:
                    if col != def_collection:
                        col.unassign(bone)

            # Task: Move MCH bones to 'MCH' collection
            if self.move_mch_to_collection and bone.name.startswith("MCH_"):
                # Assign to MCH collection
                mch_collection.assign(bone)
                
                # Remove from all other collections
                for col in arm_data.collections:
                    if col != mch_collection:
                        col.unassign(bone)

            # Task: Move CTRL bones to 'CTRL' collection
            if self.move_ctrl_to_collection and bone.name.startswith("CTRL_"):
                # Assign to CTRL collection
                ctrl_collection.assign(bone)
                
                # Remove from all other collections
                for col in arm_data.collections:
                    if col != ctrl_collection:
                        col.unassign(bone)
        # Task: Clean symmetry naming
        if self.clean_symmetry_names:
            # Map of lowercase suffix to proper capitalization
            suffix_map = {
                'l': 'L',
                'r': 'R',
                'top': 'Top',
                'bot': 'Bot',
                'fr': 'Fr',
                'bk': 'Bk'
            }
            
            for bone in arm_data.bones:
                # Check if bone ends with period or underscore followed by a symmetry suffix
                match = re.search(r'[._](l|r|top|bot|fr|bk)$', bone.name, re.IGNORECASE)
                if match:
                    suffix_lower = match.group(1).lower()
                    if suffix_lower in suffix_map:
                        # Replace with period and proper capitalization
                        new_name = bone.name[:match.start()] + '.' + suffix_map[suffix_lower]
                        bone.name = new_name

        # Task: Generate Report
        if self.generate_report:
            report_lines = []
            report_lines.append(f"=== BONE DOCTOR REPORT: {arm_obj.name} ===")
            report_lines.append(f"Generated: {bpy.context.scene.frame_current}")
            report_lines.append("")
            
            warnings_found = False
            
            # 1. IK Constraints with no targets
            ik_no_target = []
            ik_no_pole = []
            ik_zero_chain = []
            for pbone in arm_obj.pose.bones:
                for constraint in pbone.constraints:
                    if constraint.type == 'IK':
                        if not constraint.target:
                            ik_no_target.append(pbone.name)
                        if not constraint.pole_target:
                            ik_no_pole.append(pbone.name)
                        if constraint.chain_count == 0:
                            ik_zero_chain.append(pbone.name)
            
            if ik_no_target:
                warnings_found = True
                report_lines.append("- BONES WITH IK CONSTRAINTS WITH NO TARGETS:")
                for bone_name in ik_no_target:
                    report_lines.append(f"   - {bone_name}")
                report_lines.append("")
            
            if ik_no_pole:
                warnings_found = True
                report_lines.append("- BONES WITH IK CONSTRAINTS AND NO POLE TARGETS:")
                for bone_name in ik_no_pole:
                    report_lines.append(f"   - {bone_name}")
                report_lines.append("")
            
            if ik_zero_chain:
                warnings_found = True
                report_lines.append("- BONES WITH IK CONSTRAINTS WITH 0 CHAIN LENGTH:")
                for bone_name in ik_zero_chain:
                    report_lines.append(f"   - {bone_name}")
                report_lines.append("")
            
            # 4. Bones with Other Missing Constraint Targets
            missing_targets = []
            for pbone in arm_obj.pose.bones:
                for constraint in pbone.constraints:
                    if constraint.type != 'IK' and hasattr(constraint, 'target'):
                        if not constraint.target:
                            missing_targets.append(f"{pbone.name} ({constraint.type})")
            
            if missing_targets:
                warnings_found = True
                report_lines.append("- BONES WITH OTHER MISSING CONSTRAINT TARGETS:")
                for entry in missing_targets:
                    report_lines.append(f"   - {entry}")
                report_lines.append("")
            
            # # 5. Bones that are marked use_deform and have constraints
            # deform_with_constraints = []
            # for pbone in arm_obj.pose.bones:
            #     if arm_data.bones[pbone.name].use_deform and len(pbone.constraints) > 0:
            #         deform_with_constraints.append(pbone.name)
            
            # if deform_with_constraints:
            #     warnings_found = True
            #     report_lines.append("- BONES THAT ARE MARKED USE_DEFORM AND HAVE CONSTRAINTS:")
            #     for bone_name in deform_with_constraints:
            #         report_lines.append(f"   - {bone_name}")
            #     report_lines.append("")
            
            # 6. CTRL_ or CTL_ bones that do not have a custom shape
            ctrl_no_shape = []
            for pbone in arm_obj.pose.bones:
                if (pbone.name.startswith("CTRL_") or pbone.name.startswith("CTL_")):
                    if not pbone.custom_shape:
                        ctrl_no_shape.append(pbone.name)
            
            if ctrl_no_shape:
                warnings_found = True
                report_lines.append("- CTRL_/CTL_ BONES WITHOUT CUSTOM SHAPES:")
                for bone_name in ctrl_no_shape:
                    report_lines.append(f"   - {bone_name}")
                report_lines.append("")
            
            # 7. Pose Bones with negative scale
            negative_scale = []
            for pbone in arm_obj.pose.bones:
                if any(s < 0 for s in pbone.scale):
                    negative_scale.append(pbone.name)
            
            if negative_scale:
                warnings_found = True
                report_lines.append("- POSE BONES WITH NEGATIVE SCALE:")
                for bone_name in negative_scale:
                    report_lines.append(f"   - {bone_name}")
                report_lines.append("")
            

            # List Bones that do not start with DEF_, CTRL_, or MCH_
            non_def_ctrl_mch = []
            for bone in arm_data.bones:
                if not (bone.name.startswith("DEF_") or bone.name.startswith("CTRL_") or bone.name.startswith("MCH_")):
                    non_def_ctrl_mch.append(bone.name)
            
            if non_def_ctrl_mch:
                warnings_found = True
                report_lines.append("- BONES THAT DO NOT START WITH DEF_, CTRL_, OR MCH_")
                for bone_name in non_def_ctrl_mch:
                    report_lines.append(f"   - {bone_name}")
                report_lines.append("")


            # # 8. IK Bones which are parented to the bone with the IK constraint, or within chain
            # ik_parenting_issues = []
            # for pbone in arm_obj.pose.bones:
            #     for constraint in pbone.constraints:
            #         if constraint.type == 'IK':
            #             if constraint.target == arm_obj and constraint.subtarget:
            #                 # Get the IK target bone
            #                 ik_target_bone = arm_obj.pose.bones.get(constraint.subtarget)
            #                 if ik_target_bone:
            #                     # Check if IK target is parented to this bone or within chain
            #                     parent = ik_target_bone.parent
            #                     chain_depth = 0
            #                     max_chain = constraint.chain_count if constraint.chain_count > 0 else 999
                                
            #                     while parent and chain_depth < max_chain:
            #                         if parent == pbone:
            #                             ik_parenting_issues.append(f"{pbone.name} (IK target: {constraint.subtarget})")
            #                             break
            #                         parent = parent.parent
            #                         chain_depth += 1
            
            # if ik_parenting_issues:
            #     warnings_found = True
            #     report_lines.append("- IK BONES PARENTED WITHIN IK CHAIN:")
            #     for entry in ik_parenting_issues:
            #         report_lines.append(f"   - {entry}")
            #     report_lines.append("")
            
            # 9. DEF Bones with transform locks
            def_with_locks = []
            for pbone in arm_obj.pose.bones:
                if pbone.name.startswith("DEF_"):
                    has_locks = (any(pbone.lock_location) or 
                                any(pbone.lock_rotation) or 
                                any(pbone.lock_scale))
                    if has_locks:
                        def_with_locks.append(pbone.name)
            
            if def_with_locks:
                warnings_found = True
                report_lines.append("- DEF BONES WITH TRANSFORM LOCKS:")
                for bone_name in def_with_locks:
                    report_lines.append(f"   - {bone_name}")
                report_lines.append("")
            
            # Other Checks: Multiple root bones
            root_bones = [bone for bone in arm_data.bones if not bone.parent]
            if len(root_bones) > 1:
                warnings_found = True
                report_lines.append("- OTHER CHECKS:")
                report_lines.append("- ARMATURE DOES NOT HAVE A SINGLE ROOT BONE:")
                report_lines.append(f"   Found {len(root_bones)} root bones:")
                for bone in root_bones:
                    report_lines.append(f"   - {bone.name}")
                report_lines.append("")
            
            # Other Checks: All bones in default "Bones" collection
            bones_collection = arm_data.collections.get("Bones")
            if bones_collection:
                # Check if all bones are only in this collection
                all_in_bones_only = True
                for bone in arm_data.bones:
                    # Check if bone is in "Bones" collection
                    in_bones = bone.name in bones_collection.bones
                    # Check if bone is in any other collection
                    in_other = any(bone.name in col.bones for col in arm_data.collections if col.name != "Bones")
                    
                    if not in_bones or in_other:
                        all_in_bones_only = False
                        break
                
                if all_in_bones_only and len(arm_data.bones) > 0:
                    warnings_found = True
                    if len(root_bones) <= 1:  # Only add header if not already added
                        report_lines.append("- OTHER CHECKS:")
                    report_lines.append("- ALL BONES ARE ASSIGNED TO DEFAULT 'BONES' COLLECTION:")
                    report_lines.append("   Consider organizing bones into meaningful collections (DEF, CTRL, MCH, etc.)")
                    report_lines.append("")
            
            if not warnings_found:
                report_lines.append("No warnings found! Armature looks good.")
            
            # Create or update text datablock
            report_name = f"{arm_obj.name}_Report"
            if report_name in bpy.data.texts:
                text_block = bpy.data.texts[report_name]
                text_block.clear()
            else:
                text_block = bpy.data.texts.new(report_name)
            
            text_block.write("\n".join(report_lines))

            # `output an INFO  message to the user with the name of the report with self.report
            self.report({'INFO'}, f"Report saved to text block: {report_name}")
            
            
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ARMATURE_OT_bone_doctor)

def unregister():
    bpy.utils.unregister_class(ARMATURE_OT_bone_doctor)
