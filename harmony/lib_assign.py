import bpy  # type: ignore
from math import pow  # Ensure pow is imported
from . import harmony_settings


def setNode(mat, props):
    if mat.node_tree.nodes.get(props.target_bsdf_node_name) is None:
        props.target_bsdf_node_name = ""
    elif (
        mat.node_tree.nodes.get(props.target_bsdf_node_name).type
        not in harmony_settings.type_list
    ):
        props.target_bsdf_node_name = ""

    if not props.target_bsdf_node_name:
        for node in mat.node_tree.nodes:
            if node.type in harmony_settings.type_list:
                props.target_bsdf_node_name = node.name
                break


def checkObMat(self, context, obj):
    if not obj:
        self.report({"WARNING"}, "No active object selected.")
        return (False, None, None)

    if obj.type == "LIGHT" and obj.data.use_nodes and obj.data.node_tree:
        return (True, obj, obj.data)

    mat = obj.active_material
    if not mat:
        self.report({"WARNING"}, obj.name + " has no active material.")
        return (False, obj, None)
    if not mat.use_nodes:
        self.report({"WARNING"}, "Material on " + obj.name + " does not use nodes.")
        return (False, obj, mat)
    return (True, obj, mat)