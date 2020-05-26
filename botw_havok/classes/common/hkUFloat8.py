from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt8

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkUFloat8(hkObject):
    value: UInt8

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.value = br.read_uint8()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_uint8(self.value)

    def as_dict(self):
        return {"value": self.value}

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.value = d["value"]

        return inst
