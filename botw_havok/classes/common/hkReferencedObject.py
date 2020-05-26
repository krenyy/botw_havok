from typing import TYPE_CHECKING

from .hkBaseObject import hkBaseObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkReferencedObject(hkBaseObject):
    memSizeAndRefCount: UInt32

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        self.memSizeAndRefCount = br.read_uint32()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        bw.write_uint32(UInt32(self.memSizeAndRefCount))

    def as_dict(self):
        return {"memSizeAndRefCount": self.memSizeAndRefCount}

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.memSizeAndRefCount = UInt32(d["memSizeAndRefCount"])
        return inst
