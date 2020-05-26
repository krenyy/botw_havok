from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt64

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkSimplePropertyValue(hkObject):
    data: UInt64

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.data = br.read_uint64()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_uint64(UInt64(self.data))

    def as_dict(self):
        return {"data": self.data}

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.data = d["data"]

        return inst
