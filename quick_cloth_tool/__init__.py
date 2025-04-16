# __init__.py

bl_info = {
    "name": "Quick Cloth Tool",
    "author": "Johnny Matthews",
    "version": (1, 0, 3),
    "blender": (4, 4, 0),
    "description": "Adds a cloth modifier and creates a Pinning group from selected vertices.",
    "category": "Object",
}

from . import operators
from . import ui

def register():
    operators.register()
    ui.register()

def unregister():
    operators.unregister()
    ui.unregister()

if __name__ == "__main__":
    register()