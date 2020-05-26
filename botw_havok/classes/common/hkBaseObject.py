from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkBaseObject(hkObject):
    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        hkFile._assert_pointer(br)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        hkFile._write_empty_pointer(bw)

    def __repr__(self):
        return f"{self.__class__.__name__}()"
