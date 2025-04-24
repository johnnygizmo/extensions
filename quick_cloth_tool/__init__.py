# __init__.py

bl_info = {
    "name": "Quick Cloth Tool",
    "author": "Johnny Matthews",
    "version": (1, 0, 6),
    "blender": (4, 4, 0),
    "description": "Adds a cloth modifier and creates a Pinning group from selected vertices.",
    "category": "Object",
}

from . import operators
from . import pillow
from . import ui
from . import drag

def register():
    operators.register()
    pillow.register()
    ui.register()
    drag.register()

def unregister():
    operators.unregister()
    pillow.unregister()
    ui.unregister()
    drag.unregister()

if __name__ == "__main__":
    register()