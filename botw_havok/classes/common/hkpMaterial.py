from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Float16, Float32, Int8
from ..enums.ResponseType import ResponseType

if False:
    from ...hkfile import HKFile


class hkpMaterial:
    responseType: Int8
    rollingFrictionMultiplier: Float16
    friction: Float32
    restitution: Float32

    def deserialize(self, hkFile: "HKFile", br: BinaryReader):
        self.responseType = br.read_int8()
        br.align_to(2)

        self.rollingFrictionMultiplier = br.read_float16()
        self.friction = br.read_float32()
        self.restitution = br.read_float32()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter):
        bw.write_int8(self.responseType)
        bw.align_to(2)

        bw.write_float16(self.rollingFrictionMultiplier)
        bw.write_float32(self.friction)
        bw.write_float32(self.restitution)

    def asdict(self):
        return {
            "responseType": ResponseType(self.responseType).name,
            "rollingFrictionMultiplier": self.rollingFrictionMultiplier,
            "friction": self.friction,
            "restitution": self.restitution,
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.responseType = getattr(ResponseType, d["responseType"]).value
        inst.rollingFrictionMultiplier = d["rollingFrictionMultiplier"]
        inst.friction = d["friction"]
        inst.restitution = d["restitution"]

        return inst
