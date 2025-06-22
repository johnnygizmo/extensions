import bpy # type: ignore


class MARVELLESSDESIGNER_OT_quick_cloth_set_stitch(bpy.types.Operator):
    """Adds a collision modifier to the selected object."""
    bl_idname = "object.marvel_less_set_stitch"
    bl_label = "Add Stich Attribute"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        for obj in context.selected_objects:
            obj.data.update()
            bpy.ops.object.mode_set(mode='OBJECT')  
            if obj and obj.type == 'MESH':
                # Ensure the "stitch" attribute exists
                if "stitch" not in obj.data.attributes:
                    obj.data.attributes.new(name="stitch", type='INT', domain='POINT')
                    pts = obj.data.attributes["stitch"]
                    for i in range(len(pts.data)):
                        pts.data[i].value = -1     

        max_stitch_value = 0
        for obj in context.selected_objects:
            if obj and obj.type == 'MESH':
                pts = obj.data.attributes["stitch"]
                for i in range(len(pts.data)):
                    max_stitch_value = max(max_stitch_value, pts.data[i].value)                         

        for obj in context.selected_objects:
            if obj and obj.type == 'MESH':      # Update the mesh data to ensure the attribute is available
                
                selected_verts = [v.index for v in obj.data.vertices if v.select]
                if selected_verts:
                    # Get the stitch attribute                    
                    pts = obj.data.attributes["stitch"]
                    if pts:
                        for vert_index in selected_verts:
                            pts.data[vert_index].value = max_stitch_value + 1
                            
            obj.data.update()
        bpy.ops.object.mode_set(mode='EDIT')  
        return {'FINISHED'}
    
class MARVELLESSDESIGNER_OT_quick_cloth_clear_stitch(bpy.types.Operator):
    """Adds a collision modifier to the selected object."""
    bl_idname = "object.marvel_less_clear_stitch"
    bl_label = "Add Stich Attribute"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        for obj in context.selected_objects:
            obj.data.update()
            bpy.ops.object.mode_set(mode='OBJECT')  
            if obj and obj.type == 'MESH':
                # Ensure the "stitch" attribute exists
                if "stitch" not in obj.data.attributes:
                    obj.data.attributes.new(name="stitch", type='INT', domain='POINT')
                    pts = obj.data.attributes["stitch"]
                    for i in range(len(pts.data)):
                        pts.data[i].value = -1     
                     

        for obj in context.selected_objects:
            if obj and obj.type == 'MESH':  
                selected_verts = [v.index for v in obj.data.vertices if v.select]
                if selected_verts:
                    pts = obj.data.attributes["stitch"]
                    if pts:
                        for vert_index in selected_verts:
                            pts.data[vert_index].value = -1
                            
            obj.data.update()
        bpy.ops.object.mode_set(mode='EDIT')  
        return {'FINISHED'}

      
def register():
    bpy.utils.register_class(MARVELLESSDESIGNER_OT_quick_cloth_set_stitch)
    bpy.utils.register_class(MARVELLESSDESIGNER_OT_quick_cloth_clear_stitch)

def unregister():
    bpy.utils.unregister_class(MARVELLESSDESIGNER_OT_quick_cloth_clear_stitch)
    bpy.utils.unregister_class(MARVELLESSDESIGNER_OT_quick_cloth_set_stitch)    