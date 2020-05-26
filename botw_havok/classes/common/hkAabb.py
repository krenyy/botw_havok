from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Vector4

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkAabb(hkObject):
    min: Vector4
    max: Vector4

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.min = br.read_vector4()
        self.max = br.read_vector4()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_vector(self.min)
        bw.write_vector(self.max)

    def as_dict(self):
        return {
            "min": self.min.as_dict(),
            "max": self.max.as_dict(),
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()

        inst.min = Vector4.from_dict(d["min"])
        inst.max = Vector4.from_dict(d["max"])

        return inst
