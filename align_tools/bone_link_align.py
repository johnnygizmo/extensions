import bpy


class ARMATURE_OT_align_connected_children(bpy.types.Operator):
    bl_idname = "armature.align_connected_children"
    bl_label = "Align Connected Bone Children"
    bl_description = (
        "Align all connected child bones (down the tree) to the direction of the selected bone, "
        "preserving original bone lengths. Optionally copy the roll of the selected bone."
    )
    bl_options = {"REGISTER", "UNDO"}

    copy_roll: bpy.props.BoolProperty(
        name="Copy Roll",
        description="Copy the selected bone's roll to all aligned children",
        default=False,
    )

    copy_length: bpy.props.BoolProperty(
        name="Copy Length",
        description="Copy the selected bone's length to all aligned children",
        default=False,
    )

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Active object must be an armature in Edit Mode.")
            return {'CANCELLED'}
        if context.mode != 'EDIT_ARMATURE':
            self.report({'ERROR'}, "Operator must be run in Armature Edit Mode.")
            return {'CANCELLED'}

        arm = obj.data
        edit_bones = arm.edit_bones
        selected = [b for b in edit_bones if b.select]
        if len(selected) != 1:
            self.report({'ERROR'}, "Select exactly one bone in Edit Mode.")
            return {'CANCELLED'}

        root = selected[0]
        direction = root.tail - root.head
        if direction.length == 0.0:
            self.report({'ERROR'}, "Selected bone has zero length; cannot determine direction.")
            return {'CANCELLED'}
        direction = direction.normalized()

        # Pre-collect original lengths for all connected descendants so modifications
        # don't affect length readings for deeper bones.
        orig_lengths = {}
        root_length = root.length

        def collect_lengths(parent):
            for child in parent.children:
                if not child.use_connect:
                    continue
                orig_lengths[child.name] = child.length
                collect_lengths(child)

        collect_lengths(root)

        def recurse(parent):
            for child in parent.children:
                # stop this branch if child is not connected
                if not child.use_connect:
                    continue

                # determine which length to use
                if self.copy_length:
                    target_len = root_length
                else:
                    # get preserved original length from pre-collected values
                    target_len = orig_lengths.get(child.name, child.length)

                # ensure head sits at parent.tail
                child.head = parent.tail.copy()

                # set tail along direction using target length
                child.tail = child.head + direction * target_len

                if self.copy_roll:
                    child.roll = root.roll

                # recurse into children of this child
                recurse(child)

        recurse(root)
        return {'FINISHED'}


def draw(self, context):
    self.layout.separator()
    self.layout.operator(ARMATURE_OT_align_connected_children.bl_idname)


def register():
    bpy.utils.register_class(ARMATURE_OT_align_connected_children)
    


def unregister():
    bpy.utils.unregister_class(ARMATURE_OT_align_connected_children)
