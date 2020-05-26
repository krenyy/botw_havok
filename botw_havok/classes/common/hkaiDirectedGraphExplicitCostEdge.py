from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Float16, UInt16, UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkaiDirectedGraphExplicitCostEdge(hkObject):
    cost: Float16
    flags: UInt16
    target: UInt32

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.cost = br.read_float16()
        self.flags = br.read_uint16()
        self.target = br.read_uint32()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_float16(self.cost)
        bw.write_uint16(self.flags)
        bw.write_uint32(self.target)
