# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy # type: ignore
from . import create_materials

class PHYSICALLYBASED_PT_main_panel(bpy.types.Panel):
    """Main panel for Physically Based Materials extension"""
    bl_label = "Physically Based Materials"
    bl_idname = "PHYSICALLYBASED_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Physically Based'
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Material Library:")
        layout.operator("physicallybased.create_materials", text="Download & Create Materials")


def register():
    create_materials.register()
    bpy.utils.register_class(PHYSICALLYBASED_PT_main_panel)


def unregister():
    bpy.utils.unregister_class(PHYSICALLYBASED_PT_main_panel)
    create_materials.unregister()
