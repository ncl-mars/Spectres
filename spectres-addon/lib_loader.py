import bpy
import os
import sys
import importlib
from pathlib import Path
from enum import Enum, IntEnum
from dataclasses import dataclass
from .utils import CollectionUtils as ColUtils

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
INDEX_OBJECT_NAME = 1

# ------------------------------------------------------------------- Module's var
module = sys.modules[__name__]
program = None
root_col = None


def clear_node_tree(node_tree):
    for node in node_tree.nodes :
        if node.type == 'GROUP':
            if node.node_tree : 
                clear_node_tree(node.node_tree)
                bpy.data.node_groups.remove(node.node_tree)


# ---------------------------------------------------- Clear SP.LIB sub collection
def clear_sp_col_from_type(lib_type):

    sp_col = bpy.data.collections.get(lib_type.idname)

    if sp_col :
        for child in sp_col.children:
            for obj in child.objects:
                if obj.type   == 'ARMATURE' : bpy.data.armatures.remove(obj.data)
                elif obj.type == 'LIGHT'    : bpy.data.lights.remove(obj.data)
                elif obj.type == 'CAMERA'   : bpy.data.cameras.remove(obj.data)
                elif obj.type == 'MATERIAL' : bpy.data.materials.remove(obj.data)
                elif obj.type == 'CURVE'    : bpy.data.curves.remove(obj.data)

                elif obj.type == 'FONT'     :
                    if obj.data.font : bpy.data.fonts.remove(obj.data.font)
                    if obj.data.materials :
                        if obj.data.materials[0] : bpy.data.materials.remove(obj.data.materials[0])

                    bpy.data.curves.remove(obj.data)

                elif obj.type == 'MESH'     : 
                    for slot in obj.material_slots :
                        mat = slot.material
                        if mat.use_nodes: clear_node_tree(mat.node_tree)
                        bpy.data.materials.remove(mat)

                    bpy.data.meshes.remove(obj.data)

                    for txt in bpy.data.texts :
                        if txt.users == 0 and txt.name.split('.')[0] == lib_type.prefix: 
                            bpy.data.texts.remove(txt)

                    for grease in bpy.data.grease_pencils :
                        if grease.users == 0 and grease.name.split('.')[0] == lib_type.prefix: 
                            bpy.data.grease_pencils.remove(grease)

                elif obj.type == 'OBJECT'   : bpy.data.objects.remove(obj)

            bpy.data.collections.remove(child, do_unlink = True)
        bpy.data.collections.remove(sp_col, do_unlink = True)

        if lib_type == LibTypes.SHADERS :
            for world in bpy.data.worlds :
                if world.name.split('.')[0] == "SL" :
                    if world.users == 0 : bpy.data.worlds.remove(world)


# -------------------------------------------------------------- Loading stage
def add_col_to_data(data_from, data_to, col_name):
    for col in data_from.collections :
        if col == col_name:
            data_to.collections.append(col)
    return data_to

def add_worlds_to_data(data_from, data_to):
    for world in data_from.worlds:
        if world.split('.')[0] == 'SL' :
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
