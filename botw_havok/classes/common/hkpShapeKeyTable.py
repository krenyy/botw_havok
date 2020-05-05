from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32
from .hkObject import hkObject

# from .hkpShapeKeyTableBlock import hkpShapeKeyTableBlock


if False:
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

    def asdict(self):
        return {
            # "lists": self.lists.asdict(),
            "occupancyBitField": self.occupancyBitField,
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()

        # inst.lists = hkpShapeKeyTableBlock.fromdict(d['lists'])
        inst.occupancyBitField = d["occupancyBitField"]

        return inst
