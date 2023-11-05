# ------------------------------------------------------------------------
#    Static utils classes
# ------------------------------------------------------------------------
import bpy
from enum import Enum, IntEnum
import os
import sys
import importlib
from pathlib import Path
from dataclasses import dataclass





class PathsUtils:

    @classmethod
    def get_child_directory(self, dir_path_to_search, name_to_search = 'datalib'):

        for directory in self.get_immediate_subdirectories(dir_path_to_search):
            if directory == name_to_search:
                return os.path.join(dir_path_to_search,directory) 
        
        return None

    @classmethod
    def search_parent_up_hierarchy(self, purepath, nameid = 'user', separator = '-'):

        for i in range(0, len(purepath.parents), 1):

            split_dir_name = os.path.basename(purepath.parents[i])

            if split_dir_name == "datalib":
                return purepath.parents[i]

            split_dir_name = split_dir_name.split(separator)
                    
            if len(split_dir_name)>1:
                if split_dir_name[0]== nameid:
                    return purepath.parents[i].parent


            else: continue

        return None

    @classmethod
    def get_list_ids_from_idnames(self, a_dir, separator = '-'):
        ids = []
        for file in os.listdir(a_dir):
            filename = os.fsdecode(file)
            if filename.endswith(".blend"): 
                proj_ids = filename.removesuffix(".blend")

                proj_ids = proj_ids.split(separator)
                if len(proj_ids) > 1 :
                    ids.append(int(proj_ids[1]))
                else: continue
            else: continue
        return ids

    @classmethod
    def get_immediate_subdirectories(self, a_dir):
        return [name for name in os.listdir(a_dir)
                if os.path.isdir(os.path.join(a_dir, name))]


class CollectionUtils(PathsUtils):

    @classmethod
    def clear_collection(self, collection = None, do_purge = True):
        bpy.data.collections.remove(collection)
        if do_purge: 
            bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

    @classmethod
    def get_collection(self, name = ""):
        
        for col in bpy.data.collections:
            if col.name == name:
                return col
        return None

    @classmethod
    def get_in_lib_data_load(self, data_from, name = ""):
        
        for col in data_from.collections:
            if col == name:
                return col
        return None


    @classmethod
    def create_linked_collection(self, parent = None, name = ""):
        collection = bpy.data.collections.new(name)
        parent.children.link(collection)

        return collection

    @classmethod
    def check_create_collection(self, parent = None, name = "", color = 'NONE', override = True):

        collection = self.get_collection(name)

        if(collection != None): 
            if override:
                self.clear_collection(collection)
                collection = self.create_linked_collection(parent, name)
            else :
                return collection

        else : collection = self.create_linked_collection(parent, name)

        collection.color_tag = color

        return collection

    
    @classmethod
    def get_collection_from_name(self, name):
        for collection in bpy.data.collections:
            if collection.name == name : return collection
        return None



class NodesUtils():

    @classmethod
    def reset_mod_to_default(self, obj, mod):
        node_tree = mod.node_group
        obj.modifiers.remove(mod)

        p_sel_obj = bpy.context.view_layer.objects.active
        ctx_obj = bpy.context.scene.objects[obj.name]
        bpy.context.view_layer.objects.active = ctx_obj

        bpy.data.objects[obj.name].modifiers.new(node_tree.name,type='NODES')
        bpy.data.objects[obj.name].modifiers[node_tree.name].node_group = node_tree

        bpy.context.view_layer.objects.active = p_sel_obj

    @classmethod
    def set_lib_time_empty_inputs(self, data_to = None, time_3d = None):
 
        for col in data_to.collections:
            for obj in col.objects:
                for mod in obj.modifiers :

                    if mod.type == 'NODES':
                        node_tree = mod.node_group

                        for i in node_tree.inputs:
                            split_name = i.name.split("_")

                            if split_name[0] == 'time' and split_name[1] == 'empty':
                                i.default_value = time_3d.arrows[int(split_name[2])]
                        
                        self.reset_mod_to_default(obj, mod)

