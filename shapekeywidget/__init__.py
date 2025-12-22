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

from . import widget_driver_panel
from . import create_widget_driver

bl_info = {
    "name": "ShapeKeyWidget",
    "author": "AUTHOR_NAME",
    "description": "Shape Key Widget Tools",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "View3D > Sidebar > Rigging",
    "warning": "",
    "category": "Rigging",
}




def register():
    widget_driver_panel.register()
    create_widget_driver.register()

def unregister():
    widget_driver_panel.unregister()
    create_widget_driver.unregister()