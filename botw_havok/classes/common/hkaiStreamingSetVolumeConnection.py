from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Int32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkaiStreamingSetVolumeConnection(hkObject):
    cellIndex: Int32
    oppositeCellIndex: Int32

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.cellIndex = br.read_int32()
        self.oppositeCellIndex = br.read_int32()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_int32(self.cellIndex)
        bw.write_int32(self.oppositeCellIndex)
