from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Vector4
from .hkObject import hkObject

if False:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkAabb(hkObject):
    min: Vector4
    max: Vector4

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.min = br.read_vector4()
        self.max = br.read_vector4()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_vector4(self.min)
        bw.write_vector4(self.max)

    def asdict(self):
        return {
            "min": self.min.asdict(),
            "max": self.max.asdict(),
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()

        inst.min = Vector4.fromdict(d["min"])
        inst.max = Vector4.fromdict(d["max"])

        return inst
