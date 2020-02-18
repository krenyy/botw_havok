from enum import Enum


class ForceCollideOntoPpuReasons(Enum):
    FORCE_PPU_USER_REQUEST = 1
    FORCE_PPU_SHAPE_REQUEST = 2
    FORCE_PPU_MODIFIER_REQUEST = 4
    FORCE_PPU_SHAPE_UNCHECKED = 8
