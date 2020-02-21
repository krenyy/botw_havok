from ...binary import BinaryReader, BinaryWriter
from ...util import Vector4

if False:
    from ...hk import HK


class hkAabb:
    min: Vector4
    max: Vector4

    def deserialize(self, hk: "HK", br: BinaryReader):
        self.min = br.read_vector4()
        self.max = br.read_vector4()

    def serialize(self, hk: "HK", bw: BinaryWriter):
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
