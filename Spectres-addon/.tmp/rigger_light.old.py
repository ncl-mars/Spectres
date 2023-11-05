import bpy
import os
import sys
from dataclasses import dataclass

from .commons import CollectionUtils as ColUtils

from .lib_data import LibTypes


module = sys.modules[__name__]
program = None


riggs = []

# ---------------------------------------------------- Blender classes
class PT_LRigger(bpy.types.Panel):

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ENSCI-tools"

    bl_idname = "VIEW_PT_navigation_panel"
    bl_label = "Light Rigger"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object
        
        riggerbox = layout.box()
        row = riggerbox.row()

        label = ""
        if obj != None : label = label + "{}".format(obj.name)
        else : label = "No target selected"
        row.label(text=label)
        
        label = ""
        if obj != None :
            if int(obj.light_rigger.mode) == 0 :
                label = "UNRIGGED"
            else:
                label = label + "RIGGED : {}".format(obj.light_rigger.mode)
        row.label(text=label)

        box = riggerbox.box()
        if obj : box.prop(obj.light_rigger, 'mode')
        
        box = riggerbox.box()


#-- 
class PGT_LRigger(bpy.types.PropertyGroup):

    def on_new_mode(self, context):
        self.root = ColUtils.check_create_collection(
            parent = bpy.context.scene.collection, 
            name = LibTypes.LIGHT_RIGGS.idname, 
            color = "COLOR_03", 
            override = False)

        if int(self.mode) > 0 :
            self.collection = ColUtils.check_create_collection(
                parent = self.root, 
                name = LibTypes.LIGHT_RIGGS.prefix + bpy.context.object.name, 
                color = "NONE", 
                override = False)
        
        program.lib_loader.append_module_to_collection(LibTypes.LIGHT_RIGGS, int(self.mode))

    root : bpy.props.PointerProperty(type=bpy.types.Collection)
    collection : bpy.props.PointerProperty(type=bpy.types.Collection)

    mode : bpy.props.EnumProperty(
        name= "Create",
        description= "choose studies load mode",
        items= [('0', "Unrigged", "",  "", 1),
                ('1', "One point", "",  "", 2 ),
                ('2', "Two points", "", "", 3),
                ('3', "Three points", "", "", 4),
                ('4', "Four points", "", "", 5)
        ],
        default = 1,
        options = {'SKIP_SAVE'},
        update = on_new_mode
    )

    def unregister():
        print("UNREGISTER OBJECT PRPERTY")


# # -- THIS CLASS IS GOING TO BE REMOVED !!
# class LR_OT_Arm(bpy.types.Operator):
#     bl_options = {'REGISTER', 'UNDO'}
#     bl_context = "Scene"
#     bl_idname = "scene.lr_arm"
#     bl_label = "Arm Rigg"

#     def execute(self, context):
#         # program.lib_loader.append_module(LibTypes.LIGHT_RIGGS)
#         return {'FINISHED'}



# ---------------------------------------------------- Module registration
# classes = [PGT_LRigger, PT_LRigger]
classes = [PGT_LRigger, PT_LRigger]


def register():
    print("-> register light rigger")
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.light_rigger = bpy.props.PointerProperty(type=PGT_LRigger)
    
def unregister():
    print("-> unregister light rigger")
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Object.light_rigger


def init(_program):
    module.program = _program












#______________________________________________________________________________________
# for i in range(0, len(module.riggs), 1):
#     rigg = riggs[i]

#     if rigg.is_obj_from_rigg(obj) : 
#         rigg_exists = True
#         break

#     if obj == rigg.carrier or rigg.handle or rigg.focus : 
#         rigg_exists = True
#         break

# if rigg_exists == False:
#     self.check_init_col(obj)
#     point_rigg = LightRigg(obj)
#     module.riggs.append(point_rigg)