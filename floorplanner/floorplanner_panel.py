# door_panel.py

import bpy # type: ignore
from bpy.types import Panel # type: ignore

class VIEW3D_PT_johnnygizmo_floorplanner_tools(Panel):
    """Door Tools Panel in 3D Viewport"""
    bl_label = "Planner Tools"
    bl_idname = "VIEW3D_PT_planner_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "FloorPlanner"  # This creates a "Door" tab in the N-panel
    bl_context = "mesh_edit"  # Only show in Edit Mode
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        
        if len(context.active_object.modifiers) == 0 or context.active_object.modifiers.active.type != "NODES" or not any(n.name == "Floorplanner3.0"  for n in context.active_object.modifiers.active.node_group.nodes):
            col.label(text="No Floorplanner Node Group found in active object.")
            return       
        
        row = col.row()
        row.scale_y = 1.5
        
        op = row.operator("jm_floorplanner.set_edge_length",
                          text="Set Edge Length")
        op.length = context.scene.JMFLOORPLANNER_edgeLength
        row.prop(context.scene, "JMFLOORPLANNER_edgeLength", text='')


        row = col.row(align=True)
        op = row.label(text="Walls:")
        row = col.row(align=True)
        row.scale_y = 1.5  # Make button taller

        op16 = row.operator("mesh.set_wall", text="Show Wall")
        op16.action = 1
        op16.hide = 0

        op17 = row.operator("mesh.set_wall", text="", icon='TRASH')
        op17.action = 1
        op17.hide = 1
        
        col.separator()
        row = col.row(align=True)

        row.scale_y = 1.5  # Make button taller
        op16a = row.operator("mesh.set_wall", text="Set Wall Options")
        op16a.action = 0
        op16a.extend1 = context.scene.JMFLOORPLANNER_wallExt1
        op16a.extend2 = context.scene.JMFLOORPLANNER_wallExt2
        op16a.width = context.scene.JMFLOORPLANNER_wallWidth
        op16a.centering = context.scene.JMFLOORPLANNER_wallCenter


        row = col.row(align=True)
        row.prop(context.scene, "JMFLOORPLANNER_wallWidth", text="Width")
        row = col.row(align=True)
        row.prop(context.scene, "JMFLOORPLANNER_wallCenter", text="Centering")
        row = col.row(align=True)
        row.prop(context.scene, "JMFLOORPLANNER_wallExt1", text="Extend 1")
        op30 = row.operator("mesh.set_wall_ext", text="", icon='TRACKING_FORWARDS_SINGLE')
        op30.value = True
        op30.end = 1
        op31 = row.operator("mesh.set_wall_ext", text="", icon='TRACKING_CLEAR_FORWARDS')
        op31.value = False
        op31.end = 1     



        row = col.row(align=True)
        row.prop(context.scene, "JMFLOORPLANNER_wallExt2", text="Extend 2")
        op32 = row.operator("mesh.set_wall_ext", text="", icon='TRACKING_FORWARDS_SINGLE')
        op32.value = True
        op32.end = 2
        op33 = row.operator("mesh.set_wall_ext", text="", icon='TRACKING_CLEAR_FORWARDS')
        op33.value = False
        op33.end = 2



        row = col.row(align=True)
        row.scale_y = 1.5  
        op18 = row.operator("mesh.load_edge_averages", text="Retrieve Options")

        # Button to set door attribute
        row = col.row(align=True)
        row.scale_y = 1.5  # Make button taller
        row.label(text="Doors:")
        row = col.row(align=True)
        row.scale_y = 1.5
        op4 = row.operator("mesh.set_door", text="Set", )
        op4.height = context.scene.JMFLOORPLANNER_doorHeight   
        
        op5 = row.operator("mesh.set_door", text="", icon='TRASH')
        op5.height = 0.0
        row = col.row(align=True) 
        row.scale_y = 1.5
        row.prop(context.scene, "JMFLOORPLANNER_doorHeight", text="Height") 
        row = col.row(align=True)     

        
        col.separator()

        row3 = col.row(align=True)
        row3.label(text="Windows:")
        row3 = col.row(align=True)
        row3.scale_y = 1.5  # Make button taller
        op2 = row3.operator("mesh.set_window", text="Set Window" )
        op2.base = context.scene.JMFLOORPLANNER_windowBase 
        op2.height = context.scene.JMFLOORPLANNER_windowHeight
        op3 = row3.operator("mesh.set_window", text="", icon='TRASH')
        op3.base = 0.0
        op3.height = 0.0
        op3.width = 0.0
        row = col.row(align=True)
        row.scale_y = 1.5
        row.prop(context.scene, "JMFLOORPLANNER_windowHeight", text="Height")
        row = col.row(align=True)
        row.scale_y = 1.5
        row.prop(context.scene, "JMFLOORPLANNER_windowBase", text="Base")



        # col.separator()     

        # row = col.row(align=True)
        # row.scale_y = 1.5  # Make button taller
        # row.label(text="Baseboard:")
        # row = col.row(align=True)
        # op7 = row.label(text="Side:")
        # op8 = row.operator("mesh.set_baseboard", text="L")
        # op8.action = 0
        # op8.side = 1
        # op9 = row.operator("mesh.set_baseboard", text="R")
        # op9.action = 0
        # op9.side = 2
        # op10 = row.operator("mesh.set_baseboard", text="Both")
        # op10.action = 0
        # op10.side = 3
        # op11 = row.operator("mesh.set_baseboard", text="None")
        # op11.action = 0
        # op11.side = 0  
        # row = col.row(align=True)
        # row.label(text="Caps:")
        # op12 = row.operator("mesh.set_baseboard", text="Start")
        # op12.action = 1
        # op12.cap = 1
        # op13 = row.operator("mesh.set_baseboard", text="End")
        # op13.action = 1
        # op13.cap = 2
        # op14 = row.operator("mesh.set_baseboard", text="Both")
        # op14.action = 1
        # op14.cap = 3
        # op15 = row.operator("mesh.set_baseboard", text="None")
        # op15.action = 1
        # op15.cap = 0

        # col.separator()

        # row = col.row(align=True)
        # row.scale_y = 1.5


def register():
    bpy.utils.register_class(VIEW3D_PT_johnnygizmo_floorplanner_tools)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_johnnygizmo_floorplanner_tools)
