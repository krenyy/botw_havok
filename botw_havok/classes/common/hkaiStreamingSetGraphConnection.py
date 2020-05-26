from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Float16, Int32, UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkaiStreamingSetGraphConnection(hkObject):
    nodeIndex: Int32
    oppositeNodeIndex: Int32
    edgeData: UInt32
    edgeCost: Float16

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.nodeIndex = br.read_int32()
        self.oppositeNodeIndex = br.read_int32()
        self.edgeData = br.read_uint32()
        self.edgeCost = br.read_float16()

        br.align_to(16)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_int32(self.nodeIndex)
        bw.write_int32(self.oppositeNodeIndex)
        bw.write_uint32(self.edgeData)
        bw.write_float16(self.edgeCost)

        bw.align_to(16)
