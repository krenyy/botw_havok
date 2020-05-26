from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Int32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkaiStreamingSetNavMeshConnection(hkObject):
    faceIndex: Int32
    edgeIndex: Int32
    oppositeFaceIndex: Int32
    oppositeEdgeIndex: Int32

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.faceIndex = br.read_int32()
        self.edgeIndex = br.read_int32()
        self.oppositeFaceIndex = br.read_int32()
        self.oppositeEdgeIndex = br.read_int32()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_int32(self.faceIndex)
        bw.write_int32(self.edgeIndex)
        bw.write_int32(self.oppositeFaceIndex)
        bw.write_int32(self.oppositeEdgeIndex)
