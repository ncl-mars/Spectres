# import bpy
# from enum import Enum, IntEnum
# from dataclasses import dataclass


# class LibTypes(int, Enum):
#     def __new__(cls, value, idname, prefix, mode_count):
#         obj = int.__new__(cls, value)
#         obj._value_ = value
#         obj.idname  = idname
#         obj.prefix  = prefix
#         obj.mode_count = mode_count
#         return obj

#     SHADERS     = (0, 'ShaderLib',  'SL_', 2)
#     NODES       = (1, 'NodeLib',    'NL_', 2)
#     LIGHT_RIGGS = (2, 'LightRiggs', 'LR_', 2)
#     CAM_RIGGS   = (3, 'CamRiggs',   'CR_', 2)

# # --
# @dataclass
# class LibBlock:
#     type = None
#     objects = []

#     def __init__(self, type, objects = None):
#         self.type = type
#         if objects : self.objects = objects

# # --
# @dataclass
# class LibUser:
#     carrier = None
#     blocks  = [LibBlock]

#     def __init__(self, carrier, blocks = None, type = None):
#         self.carrier = carrier
#         if blocks : self.blocks = blocks
#         elif type : self.block = [LibBlock(type = type)]

