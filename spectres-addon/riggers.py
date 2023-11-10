import bpy
import mathutils
import math
import os
import sys
from dataclasses import dataclass
from .commons import CollectionUtils as ColUtils
from .lib_loader import LibTypes

module = sys.modules[__name__]
program = None
loader = None


# ----------------------------------------------------------- ui panels
class SP_PT_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ENSCI-Tools"
    bl_idname = "VIEW3D_PT_sp_panel"
    bl_label = " ~ ENSCI | TOOLS ~ ( Spectres )"

    def draw(self, context): return None

class R_PT_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "VIEW3D_PT_sp_panel"
    bl_idname = "VIEW3D_PT_rigger_panel"
    bl_label = "Rigger"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        label = "ARM RIGG : () > { "
        if bpy.context.selected_objects : label = label + "{}".format(bpy.context.selected_objects[0].name)
        else : label = label + "Cursor"
        row.label(text = label+ ' }')

        row = layout.row()
        row.label(text="Light")
        row.operator(LR_OT_arm_add.bl_idname, text ="Create")
        row.operator(LR_OT_arms_clear.bl_idname, text ="Clear")

        row = layout.row()
        row.label(text="Cam")
        row.operator(CR_OT_arm_add.bl_idname, text = "Create")
        row.operator(CR_OT_arms_clear.bl_idname, text ="Clear")

# ------------------------------------------------------- rigg operators
class R_OT_rigg_add(bpy.types.Operator):
    bl_options = {'REGISTER', 'UNDO'}
    bl_context = "Object"

    def set_col_to_selected(self, sp_col, sel = None):
        for child_obj in sp_col.objects:
            split_name = child_obj.name.split('.')
            if len(split_name) > (loader.INDEX_OBJECT_NAME):
                if split_name[loader.INDEX_OBJECT_NAME] == 'handle':
                    if sel : child_obj.location = child_obj.location + sel[0].location + mathutils.Vector([0.0,0.0, sel[0].dimensions.z * 0.5])
                    else : child_obj.location = child_obj.location + bpy.context.scene.cursor.location


    def execute(self, context, lib_type):
        scene = context.scene
        sel = context.selected_objects

        lib_data = loader.load_lib_type(lib_type, 1)

        rigg_col = ColUtils.check_create_collection(
            parent = loader.root_col, 
            name = lib_type.idname, 
            color = lib_type.color, 
            override = False)

        if lib_data.collections :
            sp_col = lib_data.collections[0] 
            rigg_col.children.link(sp_col)
            self.set_col_to_selected(sp_col, sel)

        lib_data = None
        return {'FINISHED'}

class LR_OT_arm_add(R_OT_rigg_add):
    bl_idname = "object.lr_arm_add"
    bl_label = "Create Light Arm"
    def execute(self, context): return super().execute(context, LibTypes.LIGHT_RIGGS)

class CR_OT_arm_add(R_OT_rigg_add):
    bl_idname = "object.cr_arm_add"
    bl_label = "Create Camera Arm"
    def execute(self, context): return super().execute(context, LibTypes.CAM_RIGGS)

class R_OT_rigg_clear(bpy.types.Operator):
    bl_options = {'REGISTER', 'UNDO'}   
    bl_context = "Object"
    def execute(self, context, lib_type):
        loader.clear_sp_col(bpy.data.collections.get(lib_type.idname))
        return {'FINISHED'}

class LR_OT_arms_clear(R_OT_rigg_clear):
    bl_idname = "object.lr_arms_clear"
    bl_label = "Clear Light Arms Folder"
    def execute(self, context): return super().execute(context, LibTypes.LIGHT_RIGGS)
    def invoke(self, context, event): return context.window_manager.invoke_props_dialog(self, width = 150)

class CR_OT_arms_clear(R_OT_rigg_clear):
    bl_idname = "object.cr_arms_clear"
    bl_label = "Clear Camera Arms Folder"
    def execute(self, context): return super().execute(context, LibTypes.CAM_RIGGS)
    def invoke(self, context, event): return context.window_manager.invoke_props_dialog(self, width = 150)


# ---------------------------------------------------- Module registration
classes = [
            SP_PT_panel, 
            R_PT_panel, 
            LR_OT_arm_add, 
            LR_OT_arms_clear,
            CR_OT_arm_add,
            CR_OT_arms_clear
            ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

def init(_program):
    module.program = _program
    module.loader = _program.lib_loader

