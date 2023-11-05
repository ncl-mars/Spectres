# import bpy
# import mathutils
# from dataclasses import dataclass


# class LightRigg(object):
    
#     @dataclass
#     class Arm():
#         handle : bpy.types.Object
#         target : bpy.types.Object
#         projector : bpy.types.Object

#     handle = None
#     carrier = None
#     focus = None

#     arms = []
    
#     def create_root_struct(self):
#         print

#     def create_light_empty(self, name = "light_rigg", h_type = 'PLAIN_AXES', size = 2 ):
#         handle = bpy.data.objects.new( name, None)
#         handle.empty_display_type  = h_type
#         handle.empty_display_size   = size
#         return handle

#     def generate_rigg(self):
#         print


#     @classmethod
#     def is_obj_from_rigg(self, obj):
#         return False


#     def __init__(self, target_obj):

#         self.carrier = target_obj
#         self.handle = self.create_light_empty(str(target_obj.name) + "_HANDLE", 'SPHERE' )
#         self.focus =  self.create_light_empty(str(target_obj.name) + "_FOCUS", 'SPHERE' )

#         print("self.handle :" , self.handle)
#         print("self.is_obj_from_rigg(self.handle) :" , self.is_obj_from_rigg(self.handle))

#         self.focus.parent = self.handle
        

#         target_obj.rigg_props.collection.objects.link(self.handle)
#         target_obj.rigg_props.collection.objects.link(self.focus)
#         bpy.context.view_layer.objects.active = self.handle

#         bpy.ops.object.constraint_add(type='COPY_LOCATION')


#         self.handle.constraints["Copy Location"].target = self.carrier
#         self.handle.constraints["Copy Location"].use_offset = True

#         bpy.context.view_layer.objects.active = target_obj

    
    
#     # def register(self):
#     #     print("register Point rigger")
    
#     # def unregister(self):
#     #     print("unregister Point rigger")

    