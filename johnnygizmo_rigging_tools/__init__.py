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

from . import bone_picker
from . import mesh_bone_magnet
from . import armature_bone_magnet
from . import bone_straightener
from . import panel

def register(): 
    bone_picker.register()
    mesh_bone_magnet.register()
    armature_bone_magnet.register()
    bone_straightener.register()
    panel.register()

def unregister():
    panel.unregister()
    bone_picker.unregister()
    mesh_bone_magnet.unregister()
    armature_bone_magnet.unregister()
    bone_straightener.unregister()  
