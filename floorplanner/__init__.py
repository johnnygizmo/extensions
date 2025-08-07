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

from . import preferences
from . import set_edge
from . import set_window
from . import set_baseboard
from . import set_door
from . import set_wall
from . import floorplanner_panel
from . import set_edge_length
from . import properties
from . import copy_assets
def register(): 
    properties.register()   
    set_edge.register()
    set_window.register()
    set_baseboard.register()
    set_door.register()
    set_wall.register()
    floorplanner_panel.register()
    set_edge_length.register()
    copy_assets.register()
    preferences.register()
    

def unregister():
    set_edge_length.unregister()
    floorplanner_panel.unregister()
    set_wall.unregister()
    set_door.unregister()
    set_window.unregister()
    set_baseboard.unregister()
    set_edge.unregister()
    properties.unregister()
    copy_assets.unregister()
    preferences.unregister()