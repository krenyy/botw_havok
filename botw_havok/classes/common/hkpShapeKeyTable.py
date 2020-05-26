from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32

# from .hkpShapeKeyTableBlock import hkpShapeKeyTableBlock

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpShapeKeyTable(hkObject):
    # lists: hkpShapeKeyTableBlock  # doesn't appear to be used
    occupancyBitField: UInt32

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        hkFile._assert_pointer(br)  # empty 'lists' pointer

        self.occupancyBitField = br.read_uint32()

        if hkFile.header.padding_option:
            br.align_to(16)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        hkFile._write_empty_pointer(bw)

        bw.write_uint32(self.occupancyBitField)

        if hkFile.header.padding_option:
            bw.align_to(16)

    def as_dict(self):
        return {
            # "lists": self.lists.as_dict(),
            "occupancyBitField": self.occupancyBitField,
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()

        # inst.lists = hkpShapeKeyTableBlock.from_dict(d['lists'])
        inst.occupancyBitField = d["occupancyBitField"]

        return inst
