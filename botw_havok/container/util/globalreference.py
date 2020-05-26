from .hkobject import HKObject
from ...binary.types import Int32, UInt32


class GlobalReference:
    src_obj: HKObject
    dst_obj: HKObject

    dst_section_id: Int32

    src_rel_offset: UInt32
    dst_rel_offset: UInt32 = UInt32(0)  # Should always point to the beginning

    def __init__(self):
        self.dst_obj = HKObject()

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.src_obj.hkClass.name}@{hex(self.src_rel_offset)}, "
            f"{self.dst_obj.hkClass.name}@{hex(self.dst_rel_offset)})"
        )

    def __hash__(self):
        return hash(
            (self.src_obj, self.dst_obj, self.src_rel_offset, self.dst_rel_offset)
        )
