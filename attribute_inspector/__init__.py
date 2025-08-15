import bpy
import bmesh
from mathutils import Vector
from bpy.app.handlers import persistent

# Stores the last known selection/attribute state so we know when to refresh
_last_cache_state = None


# ------------------------------
# Data storage
# ------------------------------
class JohnnyGizmoAttributeValue(bpy.types.PropertyGroup):
    """
    A PropertyGroup to store attribute data, including name, domain,
    data type, and a value for each possible type (float, int, bool, vec, color, string).
    """
    name: bpy.props.StringProperty()
    domain: bpy.props.StringProperty()
    data_type: bpy.props.StringProperty()  # 'FLOAT', 'INT', 'BOOLEAN', 'FLOAT_VECTOR', 'FLOAT_COLOR', 'STRING'
    float_value: bpy.props.FloatProperty(name="Value")
    int_value: bpy.props.IntProperty(name="Value")
    bool_value: bpy.props.BoolProperty(name="Value")
    # This property is for 3-component vectors
    vector_value: bpy.props.FloatVectorProperty(name="Value", size=3)
    # This property is specifically for 4-component colors
    color_value: bpy.props.FloatVectorProperty(name="Value", size=4, subtype='COLOR')
    # This new property is for string attributes
    string_value: bpy.props.StringProperty(name="Value")


# ------------------------------
# Operator to set attribute value
# ------------------------------
class JOHNNYGIZMO_MESH_OT_set_attribute_value(bpy.types.Operator):
    """
    Operator to set the value of a selected attribute on the active mesh.
    It now handles float, integer, boolean, vector, color, and string attributes.
    """
    bl_idname = "mesh.johnnygizmo_set_attribute_value"
    bl_label = "Set Attribute Value"
    bl_options = {'REGISTER', 'UNDO'}

    attr_name: bpy.props.StringProperty()
    domain: bpy.props.StringProperty()
    data_type: bpy.props.StringProperty()
    value_float: bpy.props.FloatProperty()
    value_int: bpy.props.IntProperty()
    value_bool: bpy.props.BoolProperty()
    value_vector: bpy.props.FloatVectorProperty()
    value_color: bpy.props.FloatVectorProperty(size=4, default=(0.0, 0.0, 0.0, 1.0))
    value_string: bpy.props.StringProperty()

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'WARNING'}, "Active object is not a mesh.")
            return {'CANCELLED'}

        bm = bmesh.from_edit_mesh(obj.data)

        layer = None
        elems = None

        # Helper function to get the correct bmesh layer
        def get_layer(elements, data_type, attr_name):
            if data_type == 'FLOAT':
                return elements.layers.float.get(attr_name)
            elif data_type == 'INT':
                return elements.layers.int.get(attr_name)
            elif data_type == 'BOOLEAN':
                return elements.layers.bool.get(attr_name)
            elif data_type == 'FLOAT_VECTOR':
                return elements.layers.float_vector.get(attr_name)
            elif data_type == 'FLOAT_COLOR':
                return elements.layers.float_color.get(attr_name)
            elif data_type == 'STRING':
                return elements.layers.string.get(attr_name)
            return None

        # Determine the correct bmesh layer and elements
        if self.domain == 'POINT':
            elems = bm.verts
            layer = get_layer(elems, self.data_type, self.attr_name)
        elif self.domain == 'EDGE':
            elems = bm.edges
            layer = get_layer(elems, self.data_type, self.attr_name)
        else:  # FACE
            elems = bm.faces
            layer = get_layer(elems, self.data_type, self.attr_name)

        if not layer:
            self.report({'WARNING'}, f"Attribute '{self.attr_name}' not found.")
            return {'CANCELLED'}

        # Get the correct value to set based on the data type
        value_to_set = None
        if self.data_type == 'FLOAT':
            value_to_set = self.value_float
        elif self.data_type == 'INT':
            value_to_set = self.value_int
        elif self.data_type == 'BOOLEAN':
            value_to_set = self.value_bool
        elif self.data_type == 'FLOAT_VECTOR':
            value_to_set = self.value_vector
        elif self.data_type == 'FLOAT_COLOR':
            # Use the color value property
            value_to_set = self.value_color
        elif self.data_type == 'STRING':
            value_to_set = self.value_string

        # Set the value on all selected elements
        for elem in elems:
            if elem.select:
                if self.data_type != 'STRING':
                    elem[layer] = value_to_set
                else:
                    elem[layer] = value_to_set.encode('utf-8')

        bmesh.update_edit_mesh(obj.data)
        return {'FINISHED'}


# ------------------------------
# UI Panel
# ------------------------------
class JOHNNYGIZMO_VIEW3D_PT_attribute_average(bpy.types.Panel):
    """
    UI panel to display and set attribute values on selected elements.
    It now dynamically displays the correct property for each attribute's data type.
    """
    bl_label = "Attribute Inspector"
    bl_idname = "VIEW3D_PT_attribute_average"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'
    bl_context = "mesh_edit"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        layout.label(text="Float, Int, Vector, Bool, Color Only")
        if not obj or obj.type != 'MESH':
            layout.label(text="No mesh object.")
            return

        if not context.scene.attribute_values:
            layout.label(text="No supported attributes found.")
            return

        last_domain = None
        for item in context.scene.attribute_values:
            if item.data_type not in {'FLOAT', 'INT', 'BOOLEAN', 'FLOAT_VECTOR', 'FLOAT_COLOR'}:
                continue
            # Group by domain with headings
            if item.domain != last_domain:
                layout.label(text=f"{item.domain.title()} Attributes:")
                last_domain = item.domain

            row = layout.row(align=True)
            
            # Use the correct property for the data type and pass the value to the operator
            op = row.operator("mesh.johnnygizmo_set_attribute_value", text="", icon="PASTEDOWN")

            if item.data_type == 'FLOAT':
                row.prop(item, "float_value", text=item.name)
                op.value_float = item.float_value
            elif item.data_type == 'INT':
                row.prop(item, "int_value", text=item.name)
                op.value_int = item.int_value
            elif item.data_type == 'BOOLEAN':
                row.prop(item, "bool_value", text=item.name)
                op.value_bool = item.bool_value
            elif item.data_type == 'FLOAT_VECTOR':
                row.prop(item, "vector_value", text=item.name)
                op.value_vector = item.vector_value
            elif item.data_type == 'FLOAT_COLOR':
                row.prop(item, "color_value", text=item.name)
                # Correctly pass the color value property
                op.value_color = item.color_value
            # elif item.data_type == 'STRING':
            #     row.prop(item, "string_value", text=item.name)
            #     op.value_string = item.string_value
                
            # Common properties for the operator call
            op.attr_name = item.name
            op.domain = item.domain
            op.data_type = item.data_type


# ------------------------------
# Handler: updates the attribute_values cache
# ------------------------------
@persistent
def update_attribute_cache(scene):
    global _last_cache_state
    ctx = bpy.context
    obj = ctx.active_object

    # Only run in mesh edit mode on a mesh
    if not obj or obj.type != 'MESH' or ctx.mode != 'EDIT_MESH':
        if scene.attribute_values:
            scene.attribute_values.clear()
        _last_cache_state = None
        return

    bm = bmesh.from_edit_mesh(obj.data)

    sel_data = []
    
    # Dynamically build the domains to process based on the current selection mode
    domains_to_process = {}
    if {'VERT'} == bm.select_mode:
        domains_to_process['POINT'] = bm.verts
    elif {'EDGE'} == bm.select_mode:
        domains_to_process['EDGE'] = bm.edges
    elif {'FACE'} == bm.select_mode:
        domains_to_process['FACE'] = bm.faces

    # Build a hash from current selection + attributes to check for changes
    for domain_name, elements in domains_to_process.items():
        # Iterate over all possible attribute layers
        for layer_name in elements.layers.float.keys():
            sel_indices = [i for i, e in enumerate(elements) if e.select]
            sel_data.append((domain_name, 'FLOAT', layer_name, tuple(sel_indices)))
        for layer_name in elements.layers.int.keys():
            sel_indices = [i for i, e in enumerate(elements) if e.select]
            sel_data.append((domain_name, 'INT', layer_name, tuple(sel_indices)))
        for layer_name in elements.layers.bool.keys():
            sel_indices = [i for i, e in enumerate(elements) if e.select]
            sel_data.append((domain_name, 'BOOLEAN', layer_name, tuple(sel_indices)))
        for layer_name in elements.layers.float_vector.keys():
            sel_indices = [i for i, e in enumerate(elements) if e.select]
            sel_data.append((domain_name, 'FLOAT_VECTOR', layer_name, tuple(sel_indices)))
        for layer_name in elements.layers.float_color.keys():
            sel_indices = [i for i, e in enumerate(elements) if e.select]
            sel_data.append((domain_name, 'FLOAT_COLOR', layer_name, tuple(sel_indices)))
        for layer_name in elements.layers.string.keys():
            sel_indices = [i for i, e in enumerate(elements) if e.select]
            sel_data.append((domain_name, 'STRING', layer_name, tuple(sel_indices)))


    state_hash = hash(str(sel_data))

    if state_hash == _last_cache_state:
        return
    _last_cache_state = state_hash
    scene.attribute_values.clear()
    for domain_name, elements in domains_to_process.items():       
        def process_layer_type(layer_collection, data_type_str):
            for layer_name in layer_collection.keys():
                layer = layer_collection.get(layer_name)
                selected_values = [elem[layer] for elem in elements if elem.select]

                item = scene.attribute_values.add()
                item.name = layer_name
                item.domain = domain_name
                item.data_type = data_type_str

                if not selected_values:
                    # Set default values
                    if data_type_str == 'FLOAT':
                        item.float_value = 0.0
                    elif data_type_str == 'INT':
                        item.int_value = 0
                    elif data_type_str == 'BOOLEAN':
                        item.bool_value = False
                    elif data_type_str == 'FLOAT_VECTOR':
                        item.vector_value = (0.0, 0.0, 0.0)
                    elif data_type_str == 'FLOAT_COLOR':
                        # Correctly use the color value property
                        item.color_value = (0.0, 0.0, 0.0, 0.0)
                    elif data_type_str == 'STRING':
                        item.string_value = ""
                else:
                    # Calculate average and set the correct property
                    if data_type_str == 'FLOAT':
                        item.float_value = sum(selected_values) / len(selected_values)
                    elif data_type_str == 'INT':
                        item.int_value = round(sum(selected_values) / len(selected_values))
                    elif data_type_str == 'BOOLEAN':
                        item.bool_value = bool(sum(selected_values) / len(selected_values) > 0.5)
                    elif data_type_str == 'FLOAT_VECTOR':
                        avg_vec = sum(selected_values, Vector((0.0, 0.0, 0.0))) / len(selected_values)
                        item.vector_value = avg_vec
                    elif data_type_str == 'FLOAT_COLOR':
                        avg_vec = sum(selected_values, Vector((0.0, 0.0, 0.0, 0.0))) / len(selected_values)
                        # The fix: assign to the 4-component 'color_value' property
                        item.color_value = avg_vec
                    elif data_type_str == 'STRING':
                        # The fix: decode the bytes to a string
                        item.string_value = selected_values[0].decode('utf-8')

        process_layer_type(elements.layers.float, 'FLOAT')
        process_layer_type(elements.layers.int, 'INT')
        process_layer_type(elements.layers.bool, 'BOOLEAN')
        process_layer_type(elements.layers.float_vector, 'FLOAT_VECTOR')
        process_layer_type(elements.layers.float_color, 'FLOAT_COLOR')
        process_layer_type(elements.layers.string, 'STRING')


# ------------------------------
# Registration
# ------------------------------
classes = (
    JohnnyGizmoAttributeValue,
    JOHNNYGIZMO_MESH_OT_set_attribute_value,
    JOHNNYGIZMO_VIEW3D_PT_attribute_average,
)

def register():
    """Register all classes and the handler."""
    for cls in classes:
        bpy.utils.register_class(cls)

    # Attach our custom collection property to the scene
    bpy.types.Scene.attribute_values = bpy.props.CollectionProperty(type=JohnnyGizmoAttributeValue)
    bpy.app.handlers.depsgraph_update_post.append(update_attribute_cache)


def unregister():
    """Unregister all classes and the handler."""
    # Check if the handler exists before trying to remove it
    if update_attribute_cache in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(update_attribute_cache)
    
    # Check if the property exists before trying to delete it
    if hasattr(bpy.types.Scene, "attribute_values"):
        del bpy.types.Scene.attribute_values

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
