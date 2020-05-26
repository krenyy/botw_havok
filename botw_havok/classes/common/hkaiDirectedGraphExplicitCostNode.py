from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Int32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkaiDirectedGraphExplicitCostNode(hkObject):
    startEdgeIndex: Int32
    numEdges: Int32

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.startEdgeIndex = br.read_int32()
        self.numEdges = br.read_int32()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_int32(self.startEdgeIndex)
        bw.write_int32(self.numEdges)
