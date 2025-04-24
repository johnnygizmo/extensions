import bpy

def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


def main(context):
    C = bpy.context
    O = bpy.ops
    D = bpy.data
    
    
    ob = C.active_object

    if ob.type != 'MESH':
        ShowMessageBox("Use only on Mesh Objects", "Error", 'ERROR')
        return

    if ob.mode != 'EDIT':
        ShowMessageBox("Put your object in edit mode first", "Error", 'ERROR')
        return


    selected = 0
    for v in ob.data.vertices:
        if v.select == True:
            selected = 1
            break
    
    if selected == 0:
        ShowMessageBox("Select at least one vertex", "Error", 'ERROR')
        return        
    
    for mod in ob.modifiers:
        if mod.type == 'CLOTH':
            ShowMessageBox("Object already has a cloth modifier", "Error", 'ERROR')
            return         
    
    
    bpy.ops.view3d.snap_cursor_to_selected()
    O.object.editmode_toggle()
    
    O.object.editmode_toggle()
    O.object.vertex_group_assign_new()
    ob.vertex_groups.active.name = "ClothDrag"
    vertexgroup = ob.vertex_groups.active.name
    O.object.editmode_toggle()
    
    O.object.add(radius=1.0, type='EMPTY',  align='WORLD')    
    empty = C.active_object
    empty.name = "ClothDrag"
    empty.location = bpy.context.scene.cursor.location
 
    O.view3d.select(deselect_all=True)
    C.view_layer.objects.active = ob   
    ob.select_set(True) 
    
    O.object.modifier_add(type='HOOK')
    ob.modifiers.active.vertex_group = vertexgroup
    ob.modifiers.active.object = empty
    ob.modifiers.active.name = "ClothDragHook"
    
    
    O.object.modifier_add(type='CLOTH')
    ob.modifiers[-1].name = "ClothDragCloth"
    ob.modifiers[-1].settings.vertex_group_mass = vertexgroup
    ob.modifiers[-1].settings.quality = 8
    

class AddClothDrag(bpy.types.Operator):
    """Add a cloth drag-hook setup"""
    bl_idname = "object.quickcloth_clothdrag"
    bl_label = "Cloth Drag"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}

class ApplyClothDrag(bpy.types.Operator):
    """Apply a cloth drag-hook setup"""
    bl_idname = "object.quickcloth_clothdrag_apply"
    bl_label = "Apply Cloth Drag"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        C = bpy.context
        O = bpy.ops
        D = bpy.data  
        
        obj = C.active_object
        bpy.ops.object.modifier_apply(modifier="ClothDragHook")  
        bpy.ops.object.modifier_apply(modifier="ClothDragCloth")  
        
        vg = obj.vertex_groups.get("ClothDrag")
        if vg:
            obj.vertex_groups.remove(vg)
        
        obj = bpy.data.objects.get("ClothDrag")
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)    
        return {'FINISHED'}

# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(AddClothDrag)
    bpy.utils.register_class(ApplyClothDrag)


def unregister():
    bpy.utils.unregister_class(ApplyClothDrag)
    bpy.utils.unregister_class(AddClothDrag)

