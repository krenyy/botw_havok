from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Int16, Int32, UInt16

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkaiNavMeshFace(hkObject):
    startEdgeIndex: Int32
    startUserEdgeIndex: Int32
    numEdges: Int16
    numUserEdges: Int16
    clusterIndex: Int16
    padding: UInt16

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.startEdgeIndex = br.read_int32()
        self.startUserEdgeIndex = br.read_int32()
        self.numEdges = br.read_int16()
        self.numUserEdges = br.read_int16()
        self.clusterIndex = br.read_int16()
        self.padding = br.read_uint16()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_int32(self.startEdgeIndex)
        bw.write_int32(self.startUserEdgeIndex)
        bw.write_int16(self.numEdges)
        bw.write_int16(self.numUserEdges)
        bw.write_int16(self.clusterIndex)
        bw.write_uint16(self.padding)

    def as_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(d)
        return inst
