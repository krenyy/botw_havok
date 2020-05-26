from typing import TYPE_CHECKING

from .hkObject import hkObject
from ..enums.ResponseType import ResponseType
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Float16, Float32, Int8

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpMaterial(hkObject):
    responseType: Int8
    rollingFrictionMultiplier: Float16
    friction: Float32
    restitution: Float32

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.responseType = br.read_int8()
        br.align_to(2)

        self.rollingFrictionMultiplier = br.read_float16()
        self.friction = br.read_float32()
        self.restitution = br.read_float32()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_int8(self.responseType)
        bw.align_to(2)

        bw.write_float16(self.rollingFrictionMultiplier)
        bw.write_float32(self.friction)
        bw.write_float32(self.restitution)

    def as_dict(self):
        return {
            "responseType": ResponseType(self.responseType).name,
            "rollingFrictionMultiplier": self.rollingFrictionMultiplier,
            "friction": self.friction,
            "restitution": self.restitution,
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.responseType = getattr(ResponseType, d["responseType"]).value
        inst.rollingFrictionMultiplier = d["rollingFrictionMultiplier"]
        inst.friction = d["friction"]
        inst.restitution = d["restitution"]

        return inst
