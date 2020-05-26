from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt16

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpEntitySmallArraySerializeOverrideType(hkObject):
    # data: None = None
    size: UInt16
    capacityAndFlags: UInt16

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        data_offset = hkFile._assert_pointer(br)  # empty 'data' pointer

        self.size = br.read_uint16()
        self.capacityAndFlags = br.read_uint16()

        if hkFile.header.padding_option:
            br.align_to(8)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        data_offset = hkFile._write_empty_pointer(bw)

        bw.write_uint16(self.size)
        bw.write_uint16(self.capacityAndFlags)

        if hkFile.header.padding_option:
            bw.align_to(8)

    def as_dict(self):
        return {
            # "data": self.data,
            "size": self.size,
            "capacityAndFlags": self.capacityAndFlags,
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        # inst.data = d["data"]
        inst.size = d["size"]
        inst.capacityAndFlags = d["capacityAndFlags"]

        return inst
