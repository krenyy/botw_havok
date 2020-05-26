from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Int32, UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class ActorInfo(hkObject):
    HashId: UInt32
    SRTHash: Int32
    ShapeInfoStart: Int32
    ShapeInfoEnd: Int32

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.HashId = br.read_uint32()
        self.SRTHash = br.read_int32()
        self.ShapeInfoStart = br.read_int32()
        self.ShapeInfoEnd = br.read_int32()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_uint32(UInt32(self.HashId))
        bw.write_int32(Int32(self.SRTHash))
        bw.write_int32(Int32(self.ShapeInfoStart))
        bw.write_int32(Int32(self.ShapeInfoEnd))

    def as_dict(self):
        return {
            "HashId": self.HashId,
            "SRTHash": self.SRTHash,
            "ShapeInfoStart": self.ShapeInfoStart,
            "ShapeInfoEnd": self.ShapeInfoEnd,
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.HashId = UInt32(d["HashId"])
        inst.SRTHash = Int32(d["SRTHash"])
        inst.ShapeInfoStart = Int32(d["ShapeInfoStart"])
        inst.ShapeInfoEnd = Int32(d["ShapeInfoEnd"])

        return inst

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.HashId}, "
            f"{self.SRTHash}, {self.ShapeInfoStart}, "
            f"{self.ShapeInfoEnd})"
        )
