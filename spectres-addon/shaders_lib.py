import bpy
import os
import sys

from dataclasses import dataclass
from .utils import CollectionUtils as ColUtils


module = sys.modules[__name__]
program = None
loader = None

# ---------------------------------------------------------- Blender Class
class SL_PT_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = "VIEW3D_PT_sp_panel"
    bl_idname = "VIEW3D_PT_sl_panel"
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
                sp_col.hide_viewport = True
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



# ---------------------------------------------------- Module registration
classes = [SL_PT_panel, SL_PT_props, SL_OT_load, SL_OT_unload]

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
