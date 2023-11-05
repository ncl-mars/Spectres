import bpy
import os
import sys
import importlib
from pathlib import Path
from bpy.utils import resource_path
from . import lib_loader, riggers, shaders_lib

# -- ORDERED !
modules = (
    lib_loader,
    riggers,
    shaders_lib,
)

def init():
    print("!! -> initialize program")
    program = sys.modules[__name__]
    for module in modules :
        module.init(program)

def register():
    print("!! -> registering program")
    for module in modules :
        if hasattr(module, 'register'):
            module.register()

def unregister():
    print("!! -> unregistering program")
    for module in modules :
        if hasattr(module, 'unregister'):
            module.unregister()
