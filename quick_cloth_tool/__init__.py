# __init__.py

bl_info = {
    "name": "Quick Cloth Tool",
    "author": "Johnny Matthews",
    "version": (1, 0, 9),
    "blender": (4, 4, 0),
    "description": "Adds a cloth modifier and creates a Pinning group from selected vertices.",
    "category": "Object",
}

from . import cloth
from . import pillow
from . import drag
from . import collision
from . import stitching
from . import gravity
from . import ui

def register():
    cloth.register()
    pillow.register()
    drag.register()
    collision.register()
    stitching.register()
    gravity.register()
    ui.register()

def unregister():
    ui.unregister()
    gravity.unregister()
    stitching.unregister()
    collision.unregister()
    drag.unregister()
    pillow.unregister()
    cloth.unregister()

if __name__ == "__main__":
    register()