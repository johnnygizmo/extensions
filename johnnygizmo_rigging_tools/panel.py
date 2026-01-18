import bpy # type: ignore



def bone_group_picker(self, context,parent=None):
    layout = self.layout
    if parent:
        layout = parent.column(align=True)

    arm = context.active_object.data
    active_bcoll = arm.collections.active

    row = layout.row()
    row.template_bone_collection_tree()

    col = row.column(align=True)
    col.operator("armature.collection_add", icon='ADD', text="")
    col.operator("armature.collection_remove", icon='REMOVE', text="")

    col.separator()

    col.menu("ARMATURE_MT_collection_context_menu", icon='DOWNARROW_HLT', text="")

    if active_bcoll:
        col.separator()
        col.operator("armature.collection_move", icon='TRIA_UP', text="").direction = 'UP'
        col.operator("armature.collection_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

    row = layout.row()

    sub = row.row(align=True)
    sub.operator("armature.collection_assign", text="Assign")
    sub.operator("armature.collection_unassign", text="Remove")

    sub = row.row(align=True)
    sub.operator("armature.collection_select", text="Select")
    sub.operator("armature.collection_deselect", text="Deselect")


def vertex_group_picker_menu(self, context,parent=None):
    ob = context.active_object
    layout = self.layout
    if parent:
        layout = parent.column(align=True)
    group = ob.vertex_groups.active

    rows = 3
    if group:
        rows = 5

    row = layout.row()
    row.template_list("MESH_UL_vgroups", "", ob, "vertex_groups", ob.vertex_groups, "active_index", rows=rows)

    col = row.column(align=True)

    col.operator("object.vertex_group_add", icon='ADD', text="")
    props = col.operator("object.vertex_group_remove", icon='REMOVE', text="")
    props.all_unlocked = props.all = False

    col.separator()

    col.menu("MESH_MT_vertex_group_context_menu", icon='DOWNARROW_HLT', text="")

    if group:
        col.separator()
        col.operator("object.vertex_group_move", icon='TRIA_UP', text="").direction = 'UP'
        col.operator("object.vertex_group_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

    if (
            ob.vertex_groups and
            (ob.mode == 'EDIT' or
            (ob.mode == 'WEIGHT_PAINT' and ob.type == 'MESH' and ob.data.use_paint_mask_vertex))
    ):
        row = layout.row()

        sub = row.row(align=True)
        sub.operator("object.vertex_group_assign", text="Assign")
        sub.operator("object.vertex_group_remove_from", text="Remove")

        sub = row.row(align=True)
        sub.operator("object.vertex_group_select", text="Select")
        sub.operator("object.vertex_group_deselect", text="Deselect")

        layout.prop(context.tool_settings, "vertex_group_weight", text="Weight")



class VIEW3D_PT_johnnygizmo_rigging_tools(bpy.types.Panel):
    bl_label = "JohnnyGizmo Rigging Tools"
    bl_idname = "VIEW3D_PT_johnnygizmo_rigging_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rigging'

    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']

        if len(context.selected_objects) == 0:
            ob = None

        if ob and ob.type == 'MESH' and ob.mode == 'EDIT' and not ob.parent:
            (tools_head, tools_display) = layout.panel("tools_disp")
            tools_head.label(text="Mesh Rigging Tools")
            if tools_display:
                tools_display.operator("mesh.johnnygizmo_create_rig_and_assign", text="Create Parent Armature", icon='OUTLINER_OB_ARMATURE')
              
        elif ob and ob.type == 'MESH' and ob.mode == 'EDIT' and ob.parent and ob.parent.type == 'ARMATURE':
            (tools_head, tools_display) = layout.panel("tools_disp")
            tools_head.label(text="Mesh Rigging Tools")
            if tools_display:
                tools_display.operator("object.johnnygizmo_mesh_bone_magnet", text="Mesh Bone Magnet", icon='SNAP_ON')
                tools_display.operator("mesh.johnnygizmo_vertex_bone_picker", text="Vertex Bone Assignment", icon='BONE_DATA')
                # tools_display.operator("mesh.johnnygizmo_add_bone_at_selected", text="Add Bone at Selected", icon='ADD')

        
        elif ob and ob.type == 'ARMATURE' and ob.mode == 'EDIT':
            (tools_head, tools_display) = layout.panel("tools_disp")
            tools_head.label(text="Armature Rigging Tools")
            if tools_display:                
                #tools_display.operator("armature.bone_doctor", text="Bone Doctor Report", icon='SHADING_BBOX')
                tools_display.operator("jg.bone_chain_rename", text="Chain Rename", icon='FONT_DATA')
                tools_display.separator()
                tools_display.operator("armature.johnnygizmo_armature_bone_magnet", text="Armature Bone Magnet", icon='SNAP_ON')
                #tools_display.operator("armature.johnnygizmo_bone_straightener", text="Bone Straightener", icon='CURVE_PATH')
                
                tools_display.operator("armature.align_bone_to_face", text="Bone Align to Face", icon='SNAP_ON')
                tools_display.operator("armature.align_connected_children", text="Bone Chain Align", icon='SNAP_ON')
    
        elif ob and ob.type == 'ARMATURE' and ob.mode == 'OBJECT' and meshes and len(meshes) > 0:
            (tools_head, tools_display) = layout.panel("tools_disp")
            tools_head.label(text="Armature Object Rigging Tools")
            if tools_display:
                tools_display.operator("object.parent_meshes_to_nearest_bone", text="Parent Meshes to Bones", icon='SNAP_ON')

        elif ob and ob.type == 'ARMATURE' and ob.mode == 'POSE':    
            (tools_head, tools_display1) = layout.panel("tools_disp")
            tools_head.label(text="Armature Pose Rigging Tools")    
            
            if tools_display1:
                row = tools_display1.row()
                row.operator("armature.bone_doctor", text="Bone Doctor", icon='SHADING_BBOX')
                if (len(context.selected_pose_bones) >=1 ):       
                    row = tools_display1.row()
                    row.operator("jg.bone_chain_rename", text="Chain Rename", icon='FONT_DATA')                 
                if (len(context.selected_pose_bones) == 2 or len(context.selected_pose_bones) == 1):       
                    row = tools_display1.row()
                    row.label(text="Constraints")
                    row = tools_display1.row()
                    row.operator("armature.johnnygizmo_add_ik_plus", text="IK+", icon='CON_KINEMATIC')
                    row.operator("armature.johnnygizmo_add_damp_track_to_plus", text="Track To+", icon='CON_TRACKTO')
                    row = tools_display1.row()
                    row.operator("armature.johnnygizmo_add_stretch_to_plus", text="Stretch To+", icon='CON_STRETCHTO')
                    row.operator("armature.johnnygizmo_add_lock_track_to_plus", text="Lock Track+", icon='CON_LOCKTRACK')
                    tools_display1.operator("pose.constraint_add_with_targets", text="Add Constraint", icon='CON_LOCKTRACK')
                
        else:
            layout.label(text="No Tools Available", icon='ERROR')

        arm_ob = None
        arm_disp = "Active Armature"
        if ob and ob.type == 'ARMATURE':
            arm_ob = ob
        elif ob and ob.parent and ob.parent.type == 'ARMATURE':
            arm_disp = "Parent Armature"
            arm_ob = ob.parent


        if ob and ob.type == 'MESH' and not ob.parent:
            (mesh_head, mesh_display) = layout.panel("arm_disp")
            mesh_head.label(text="Mesh: "+ob.name)
            if(mesh_display):
                mesh_display.operator("mesh.johnnygizmo_create_rig_and_assign", text="Create Parent Bone", icon='BONE_DATA')   

        if ob and ob.type == 'MESH' and ob.parent and ob.parent.type == 'ARMATURE' and ob.parent_type == "BONE":
            (mesh_head, mesh_display) = layout.panel("arm_disp")
            mesh_head.label(text="Mesh: "+ob.name)
            if(mesh_display):
                mesh_display.label(text= "Parent Bone: "+arm_ob.name+" - "+ob.parent_bone)
                mesh_display.operator("object.johnnygizmo_parent_mesh_to_selected_bone", text="Change Parent Bone", icon='BONE_DATA')
               
        if arm_ob:
            (arm_head, arm_display) = layout.panel("arm_disp")
            arm_head.label(text=arm_disp+": " + arm_ob.name)
            if(arm_display):
                arm_display.row().prop(arm_ob.data, "pose_position", expand=True)
                arm_display.prop(arm_ob.data, "display_type", text="")
                r = arm_display.row()
                r.prop(arm_ob.data, "show_axes", text="Axes")
                r.prop(arm_ob.data, "axes_position", text="Position")
                arm_display.prop(arm_ob.data, "show_names", text="Bone Names")
                arm_display.prop(arm_ob, "show_in_front", text="In Front")
                arm_display.prop(arm_ob.data, "show_bone_custom_shapes", text="Custom Shapes")
                r = arm_display.row()
                r.label(text="Relations")
                r.prop_enum(arm_ob.data, "relation_line_position", "TAIL")
                r.prop_enum(arm_ob.data, "relation_line_position", "HEAD")


        if ob and  (context.active_bone or context.active_pose_bone) and ob.type == 'ARMATURE':
            bone = context.active_bone if context.active_bone else context.active_pose_bone
            (bone_head,bone_display) = layout.panel("bone_disp",default_closed=True    )
            bone_head.label(text="Active Bone: " + context.active_bone.name)
            if bone_display:
                bone_display.prop(bone, "use_deform", text="Deform")
                bone_display.prop(bone, "use_connect", text="Connect")
                bone_display.prop(bone, "use_inherit_rotation", text="Inherit Rotation")
                bone_display.prop(bone.color, "palette", text="Color Palette")

        if context.selected_pose_bones and len(context.selected_pose_bones) > 0 and ob.type == 'ARMATURE' and ob.mode == 'POSE':
            if(context.active_pose_bone):
                (pose_head,pose_display) = layout.panel("Active Pose Bone", default_closed=True)
                bone = context.active_pose_bone
                pose_head.label(text="Active Pose Bone: " + bone.name)

                if pose_display:
                    ikconstraints = [c for c in bone.constraints if c.type == 'IK']
                    
                    
                    pose_display.label(text="IK")


                    if ikconstraints and len(ikconstraints) > 0:
                        ik = ikconstraints[0]
                        pose_display.prop_search(ik, "target", context.scene, "objects", text="Target")
                        if ik.target and ik.target.type == 'ARMATURE':
                            pose_display.prop_search(ik, "subtarget", ik.target.data, "bones", text="-Bone")
                        pose_display.prop_search(ik, "pole_target", context.scene, "objects", text="Pole")
                        if ik.pole_target and ik.pole_target.type == 'ARMATURE':
                            pose_display.prop_search(ik, "pole_subtarget", ik.target.data, "bones", text="-Bone")
                            if ik.pole_subtarget:
                                pose_display.prop(ik, "pole_angle")

                        pose_display.prop(ik, "chain_count")


                    pose_display.row().prop(context.active_pose_bone, "ik_stretch", text="Stretch")
                    row = pose_display.row(align=True)
                    col = row.column(align=False)
                    col.label(text="Lock:")
                    col.label(text="Stiff:")
                    col.label(text="Limit:")
                    col.label(text="Min:")
                    col.label(text="Max:")

                    col = row.column(align=True)
                    col.prop(context.active_pose_bone, "lock_ik_x", text="X")
                    col.prop(context.active_pose_bone, "ik_stiffness_x", text="")
                    col.prop(context.active_pose_bone, "use_ik_limit_x", text="")
                    col.prop(context.active_pose_bone, "ik_min_x", text="")
                    col.prop(context.active_pose_bone, "ik_max_x", text="")

                    col = row.column(align=True)
                    col.prop(context.active_pose_bone, "lock_ik_y", text="Y")
                    col.prop(context.active_pose_bone, "ik_stiffness_y", text="")
                    col.prop(context.active_pose_bone, "use_ik_limit_y", text="")
                    col.prop(context.active_pose_bone, "ik_min_y", text="")
                    col.prop(context.active_pose_bone, "ik_max_y", text="")

                    col = row.column(align=True)
                    col.prop(context.active_pose_bone, "lock_ik_z", text="Z")
                    col.prop(context.active_pose_bone, "ik_stiffness_z", text="")
                    col.prop(context.active_pose_bone, "use_ik_limit_z", text="")
                    col.prop(context.active_pose_bone, "ik_min_z", text="")
                    col.prop(context.active_pose_bone, "ik_max_z", text="")

            (shape_head,shape_display) = layout.panel("Custom Bone Shape", default_closed=True)
            shape_head.label(text="Custom Bone Shape")
            if shape_display:
                shape_display.row().prop(context.active_pose_bone, "custom_shape", text="Shape")
                if context.active_pose_bone.custom_shape:
                    shape_display.row().prop(context.active_pose_bone, "custom_shape_translation", text="Loc")
                    shape_display.row().prop(context.active_pose_bone, "custom_shape_rotation_euler", text="Rot")
                    shape_display.row().prop(context.active_pose_bone, "custom_shape_scale_xyz", text="Scale")
                    shape_display.row().prop(context.active_pose_bone, "custom_shape_transform", text="Custom Transform")
                    shape_display.row().prop(context.active_pose_bone, "use_custom_shape_bone_size", text="Scale Bone to Length")
                    shape_display.row().prop(context.active_bone, "show_wire", text="Wire")
                    shape_display.row().prop(context.active_pose_bone, "custom_shape_wire_width", text="Wire Width")
        
        if ob and ob.type == 'MESH' and ( ob.mode == 'EDIT' or ob.mode == 'WEIGHT_PAINT'):
            (tools_head, tools_display) = layout.panel("vgroup_disp", default_closed=True)
            tools_head.label(text="Vertex Groups")
            if tools_display:
                vertex_group_picker_menu(self, context, tools_display)
    
        # if ob and ob.type == 'ARMATURE' and (ob.mode == 'EDIT' or ob.mode == 'POSE'):
        #     (tools_head, bone_group_display) = layout.panel("bone_group_disp", default_closed=True)
        #     tools_head.label(text="Bone Groups")
        #     if bone_group_display:
        #         bone_group_picker(self, context, tools_display)

def register():
    bpy.utils.register_class(VIEW3D_PT_johnnygizmo_rigging_tools)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_johnnygizmo_rigging_tools)