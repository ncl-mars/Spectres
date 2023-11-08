import bpy
import os
import sys
import importlib
from pathlib import Path
from enum import Enum, IntEnum
from dataclasses import dataclass
from .commons import CollectionUtils as ColUtils


# ------------------------------------------------------------------- LibDef
class LibTypes(int, Enum):
    def __new__(cls, value, idname, prefix, numstep, loadable, color):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.idname  = idname
        obj.prefix  = prefix
        obj.numstep = numstep
        obj.loadable = loadable
        obj.color = color
        return obj

    SHADERS     = (0, 'SP.ShaderLib',  'SL', 5, True,  'COLOR_04')
    NODES       = (1, 'SP.NodeLib',    'NL', 2, True,  'COLOR_05')
    LIGHT_RIGGS = (2, 'SP.LightRiggs', 'LR', 2, False, 'COLOR_03')
    CAM_RIGGS   = (3, 'SP.CamRiggs',   'CR', 2, False, 'COLOR_02')

# ------------------------------------------------------------------- Constants
USER = Path(bpy.utils.resource_path('USER'))
src = USER / "scripts/addons" / "Spectres-addon" # should not be hard coded
file_path = src / "Spectres-lib.blend"

ROOT_NAME = 'SP.LIB'
INDEX_OBJECT_NAME = 2

# ------------------------------------------------------------------- Module's var
module = sys.modules[__name__]
program = None
root_col = None

# ---------------------------------------------------- Clear SP.LIB sub collection
def clear_sp_col(sp_col):
    if sp_col :
        for child in sp_col.children:
            for obj in child.objects:
                print("deleting sp objects : ", obj, " of type : ", obj.type)

                if obj.type   == 'ARMATURE' : bpy.data.armatures.remove(obj.data)
                elif obj.type == 'LIGHT'    : bpy.data.lights.remove(obj.data)
                elif obj.type == 'CAMERA'   : bpy.data.cameras.remove(obj.data)
                elif obj.type == 'MATERIAL' : bpy.data.materials.remove(obj.data)
                elif obj.type == 'CURVE'    : bpy.data.curves.remove(obj.data)
                elif obj.type == 'FONT'     :
                    if obj.data.font : bpy.data.fonts.remove(obj.data.font)
                    bpy.data.curves.remove(obj.data, do_unlink = True)

                elif obj.type == 'MESH'     : 
                    for slot in obj.material_slots :
                        bpy.data.materials.remove(slot.material)
                    bpy.data.meshes.remove(obj.data)

                    for txt in bpy.data.texts :
                        if txt.users == 0 and txt.name.split('.')[0] == 'SP': 
                            bpy.data.texts.remove(txt)
                    for grease in bpy.data.grease_pencils :
                        if grease.users == 0 and grease.name.split('.')[0] == 'SP': 
                            bpy.data.grease_pencils.remove(grease)

                elif obj.type == 'OBJECT'   : bpy.data.objects.remove(obj)

            bpy.data.collections.remove(child, do_unlink = True)
        bpy.data.collections.remove(sp_col, do_unlink = True)

# -------------------------------------------------------------- Loading stage
def add_col_to_data(data_from, data_to, col_name):
    for col in data_from.collections :
        if col == col_name:
            data_to.collections.append(col)
    return data_to

def add_worlds_to_data(data_from, data_to):
    for world in data_from.worlds:
        if world.split('.')[0] == 'SP' :
            if world.split('.')[1] == 'SL' :
                data_to.worlds.append(world)
    return data_to

def load_lib_type(lib_type, id = None):

    module.root_col = ColUtils.check_create_collection(
        parent = bpy.context.scene.collection, 
        name = ROOT_NAME, 
        color = 'COLOR_01', 
        override = False)
    root_col.hide_render = True
    

    with bpy.data.libraries.load(str(file_path)) as (data_from, data_to):
        
        if lib_type == LibTypes.SHADERS :

            for i in range(0, lib_type.numstep, 1):
                data_to = add_col_to_data(data_from, data_to, "SP." + lib_type.prefix + str(i + 1))
                print("trying to add col named : ",  "SP." + lib_type.prefix + str(i + 1))

            data_to = add_worlds_to_data(data_from, data_to)

        else : data_to = add_col_to_data(data_from, data_to, "SP." + lib_type.prefix + str(id))

    return data_to

# ------------------------------------------------------------- Registration
def register():
    print
    
def unregister():
    print

def init(_program):
    print










# ---------------------------------------------------- App Events
# if lib_type == LibTypes.LIGHT_RIGGS or lib_type == LibTypes.CAM_RIGGS :

# def on_depsgraph_update(scene):
#     obj = bpy.context.active_object
#     depsgraph = bpy.context.evaluated_depsgraph_get()

#     if obj != None :
#         if obj.light_rigger.collection != None : 
#             obj.light_rigger.collection.name = "LR_" + obj.name
#     return {'FINISHED'}


# bpy.app.handlers.depsgraph_update_post.clear()
# bpy.app.handlers.depsgraph_update_post.append(on_depsgraph_update)
