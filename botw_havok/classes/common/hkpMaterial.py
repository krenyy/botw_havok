from ..enums.ResponseType import ResponseType
from ...binary import BinaryReader, BinaryWriter

if False:
    from ...hk import HK


class hkpMaterial:
    responseType: int
    rollingFrictionMultiplier: float
    friction: float
    restitution: float

    def deserialize(self, hk: "HK", br: BinaryReader):
        self.responseType = br.read_int8()
        br.align_to(2)

        self.rollingFrictionMultiplier = br.read_half()
        self.friction = br.read_single()
        self.restitution = br.read_single()

    def serialize(self, hk: "HK", bw: BinaryWriter):
        bw.write_int8(self.responseType)
        bw.align_to(2)

        bw.write_half(self.rollingFrictionMultiplier)
        bw.write_single(self.friction)
        bw.write_single(self.restitution)

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
