from typing import TYPE_CHECKING

from .hkObject import hkObject
from ..enums.EdgeFlagBits import EdgeFlagBits
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Float16, Int32, UInt8, UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkaiNavMeshEdge(hkObject):
    a: Int32
    b: Int32
    oppositeEdge: UInt32
    oppositeFace: UInt32
    flags: UInt8
    paddingByte: UInt8
    userEdgeCost: Float16

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.a = br.read_int32()
        self.b = br.read_int32()
        self.oppositeEdge = br.read_uint32()
        self.oppositeFace = br.read_uint32()
        self.flags = br.read_uint8()
        self.paddingByte = br.read_uint8()
        self.userEdgeCost = br.read_float16()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_int32(self.a)
        bw.write_int32(self.b)
        bw.write_uint32(self.oppositeEdge)
        bw.write_uint32(self.oppositeFace)
        bw.write_uint8(self.flags)
        bw.write_uint8(self.paddingByte)
        bw.write_float16(self.userEdgeCost)

    def as_dict(self):
        d = self.__dict__
        d.update({"flags": EdgeFlagBits(self.flags).name})
        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(d)

        inst.flags = EdgeFlagBits[d["flags"]].value

        return inst
