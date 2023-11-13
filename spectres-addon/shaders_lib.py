import bpy
import os
import sys

from dataclasses import dataclass
from .utils import CollectionUtils as ColUtils


module = sys.modules[__name__]
program = None
loader = None

# ---------------------------------------------------------- LOADER
class SL_PT_ui_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "VIEW3D_PT_sp_panel"
    bl_idname = "VIEW3D_PT_sl_ui_panel"
    bl_label = "Shaders Lib"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        row = layout.row()
        row.label(text= "Loaded : ")
        row.label(text="{}".format(scene.sl_props.is_loaded))
        
        if scene.sl_props.is_loaded :   
            loader = row.operator(SL_OT_unload.bl_idname, text = "Unload")
            row = layout.row()
            split = row.split(factor = 0.5,align =  True)
            split.label(text="Show Exemples")
            split.prop(scene.sl_props, 'exemples', text = "")

        else : row.operator(SL_OT_load.bl_idname, text = "Load")

class SL_PT_props(bpy.types.PropertyGroup):

    def on_exemples(self, context):
        print(self.exemples)

    is_loaded : bpy.props.BoolProperty(
        name = "isloaded",
        description = "Load State",
        default = False)
    
    exemples : bpy.props.EnumProperty(
        name= "Exemples",
        description= "Show Exemples",
        items= [
                ('0', "None", "", "", 1),
                ('1', "Texture Based", "", "", 0),
                ('2', "SDF 2D", "",  "", 3),
                ('3', "SDF 3D", "", "", 4),
                ('4', "Volumetrics", "", "", 5),
        ],
        default = 1,
        options ={'SKIP_SAVE'},
        update=on_exemples)
    
class SL_OT_loader(bpy.types.Operator):
    bl_options = {'REGISTER', 'UNDO'}
    bl_context = "Scene"

    def clear_sp_worlds(self):
        for world in bpy.data.worlds :
            split_name = world.name.split('.')
            if split_name[0] == 'SP' :
                if len(split_name) == 3 :
                    bpy.data.worlds.remove(world)

    def create_shader_col(self):
        col = ColUtils.check_create_collection(
        parent = loader.root_col, 
        name = loader.LibTypes.SHADERS.idname, 
        color = loader.LibTypes.SHADERS.color, 
        override = False)
        col.hide_render = True
        # col.hide_viewport = True
        return col

    def execute(self, context, load_lib):
        if load_lib:

            lib_data = loader.load_lib_type(loader.LibTypes.SHADERS, 1)
            shaders_col = self.create_shader_col()
            for sp_col in lib_data.collections :
                shaders_col.children.link(sp_col)
                sp_col.hide_viewport = False
            # [shaders_col.children.link(sp_col) for sp_col in lib_data.collections]

        else:
            loader.clear_sp_col_from_type(loader.LibTypes.SHADERS)
            self.clear_sp_worlds()

        bpy.context.scene.sl_props.is_loaded = load_lib
        [a.tag_redraw() for a in context.screen.areas]
        return {'FINISHED'}

class SL_OT_load(SL_OT_loader):
    bl_idname = "scene.sl_load"
    bl_label = "Load Shader Lib"
    def execute(self, context) : return super().execute(context, True)

class SL_OT_unload(SL_OT_loader):
    bl_idname = "scene.sl_unload"
    bl_label = "Unload Shader Lib"
    def execute(self, context) : return super().execute(context, False)
    def invoke(self, context, event): return context.window_manager.invoke_confirm(self, event)


# ---------------------------------------------------------- NODE TOOLS

nodes_log = "nodes log"


def get_instance(node_tree, tree_list):
    for node in node_tree.nodes :
        if node.type == 'GROUP':
            if node.node_tree : 
                split_name = node.node_tree.name.split(".")
                i1 = max(len(split_name)-1,0)
                i2 = max(len(split_name)-2,0)

                if split_name[i1] == 'Instance' or split_name[i2] == 'Instance':
                    tree_list.append(node)
                    print("Found Instance node : ", node.node_tree.name)

                get_instance(node.node_tree, tree_list)

def check_set_instancer(node_tree):
    instance_list = []
    get_instance(tree, instance_list)
    label = "Found " + str(len(instance_list)) + " instances in this tree"
    if len(instance_list) > 0:
        users = instance_list[0].users 
        if users == len(instance_list) + 1: is_instantiated = True
        elif users > len(instance_list) + 1: is_instantiated = True
        print("instance_list[0].users : ", instance_list[0].users)

def clear_node_tree(node_tree):
    for node in node_tree.nodes :
        if node.type == 'GROUP':  
            if node.node_tree : 
                clear_node_tree(node.node_tree)
                bpy.data.node_groups.remove(node.node_tree)

def is_node_tree_selected():
    if bpy.context.selected_nodes and bpy.context.scene.sl_props.is_loaded :
        if hasattr(bpy.context.selected_nodes[0], "node_tree"): return True
    return False


class SL_PT_node_panel(bpy.types.Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_idname = "VIEW3D_PT_sl_node_panel"
    bl_label = "~ ENCI | TOOLS ~"
    bl_category = "SPECTRES"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        row = layout.row()
        
        row = layout.row()
        row.operator(SL_OT_instancer_check.bl_idname, text = "Check tree for instance")
        
        label = nodes_log
        box = layout.box()
        box.label(text = label)

class SL_OT_instancer(bpy.types.Operator):
    bl_options = {'REGISTER', 'UNDO'}
    bl_context = "Scene"

class SL_OT_instancer_check(SL_OT_instancer):
    bl_idname = "scene.sl_node_instancer"
    bl_label = "Check tree for instance"

    def clone_linked(self, instance_list):
        for tree in instance_list :
            print(tree.name)

    def execute(self, context) :

        if is_node_tree_selected() :
            module.nodes_log = ""
            tree = context.selected_nodes[0].node_tree

            print("tree.name :", tree.name, " tree.users : ", tree.users)

            if tree.users == 1 :
                instance_list = [] # nodes
                get_instance(tree, instance_list)

                num_instances = len(instance_list)
                if num_instances > 0 :
                    users = instance_list[0].node_tree.users

                    if users == num_instances + 1:
                        text = "tree is already instiated, all set and ready to shape"

                        module.nodes_log += text
                        print(text)
                    
                    elif users == num_instances :
                        text = "internal Instances exists, you need to have one at top level"
                        print(text)
                        module.nodes_log += text

                    elif users > num_instances + 1 :
                        text = "making single user !"
                        print(text)
                        new_tree_instance = instance_list[0].node_tree.copy()
                        new_tree_instance.name = tree.name + ".Instance"

                        for i in range(0, len(instance_list), 1) :
                            print("instance_list[i].name : ", instance_list[i].name)
                            instance_list[i].node_tree = new_tree_instance

                        module.nodes_log += text
                  
            else :
                text = "The Instancer Node must be a unique user"
                print(text)
                module.nodes_log += text

        return {'FINISHED'}


# ---------------------------------------------------- Module registration
classes = [SL_PT_ui_panel, 
           SL_PT_props, 
           SL_OT_load, 
           SL_OT_unload,
           SL_PT_node_panel,
           SL_OT_instancer_check]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sl_props = bpy.props.PointerProperty(type=SL_PT_props)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.sl_props

def init(_program):
    module.program = _program
    module.loader = _program.lib_loader















# __________________________________________________________________________________


# class SL_OT_loader(bpy.types.Operator):
#     bl_options = {'REGISTER', 'UNDO'}
#     bl_context = "Scene"
#     bl_idname = "sl.loader"
#     bl_label = "Loader"

#     is_loaded : bpy.props.BoolProperty(
#         name = "Is Loaded",
#         description = "This checkbox triggers a Dialog Box",
#         default = False,
#     )

#     def execute(self, context):

#         scene = bpy.context.scene
#         self.is_loaded = not self.is_loaded
#         [a.tag_redraw() for a in context.screen.areas]

#         return {'FINISHED'}

#     def invoke(self, context, event):
#         if self.is_loaded : bpy.ops.sl.dialog(msg = "dialog Unloading Lib ?")
#         # else : bpy.ops.sl.dialog('EXEC_DEFAULT', msg = "dialog Unloading Lib ?")
#         return self.execute(context)
