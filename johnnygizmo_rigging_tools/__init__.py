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
from . import add_ik_plus
from . import mesh_add_bone
from . import properties
from . import add_dampedtrack_plus
from . import add_stretchto_plus
from . import add_lockedtrack_plus
from . import parent_mesh_to_bones
from . import parent_mesh_to_bone

def register(): 
    properties.register()
    bone_picker.register()
    mesh_bone_magnet.register()
    armature_bone_magnet.register()
    bone_straightener.register()
    add_ik_plus.register()
    mesh_add_bone.register()
    add_dampedtrack_plus.register()
    add_stretchto_plus.register()
    add_lockedtrack_plus.register()
    parent_mesh_to_bones.register()
    parent_mesh_to_bone.register()
    panel.register()

def unregister():
    panel.unregister()
    parent_mesh_to_bone.unregister()
    parent_mesh_to_bones.unregister()
    add_stretchto_plus.unregister()
    add_lockedtrack_plus.unregister()
    add_dampedtrack_plus.unregister()
    mesh_add_bone.unregister()
    add_ik_plus.unregister()
    bone_picker.unregister()
    mesh_bone_magnet.unregister()
    armature_bone_magnet.unregister()
    bone_straightener.unregister()  
    properties.unregister()
