from typing import TYPE_CHECKING

from .hkpBroadPhaseHandle import hkpBroadPhaseHandle
from ..enums.BroadPhaseType import BroadPhaseType
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Int8, UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpTypedBroadPhaseHandle(hkpBroadPhaseHandle):
    type: Int8
    ownerOffset: Int8
    objectQualityType: Int8
    collisionFilterInfo: UInt32

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        self.type = br.read_int8()
        self.ownerOffset = br.read_int8()
        self.objectQualityType = br.read_int8()
        br.align_to(4)

        self.collisionFilterInfo = br.read_uint32()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        bw.write_int8(Int8(self.type))
        bw.write_int8(Int8(self.ownerOffset))
        bw.write_int8(Int8(self.objectQualityType))
        bw.align_to(4)

        bw.write_uint32(UInt32(self.collisionFilterInfo))

    def as_dict(self):
        d = super().as_dict()
        d.update(
            {
                "type": BroadPhaseType(self.type).name,
                "ownerOffset": self.ownerOffset,
                "objectQualityType": self.objectQualityType,
                "collisionFilterInfo": self.collisionFilterInfo,
            }
        )

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().from_dict(d).__dict__)

        inst.type = BroadPhaseType[d["type"]].value
        inst.ownerOffset = d["ownerOffset"]
        inst.objectQualityType = d["objectQualityType"]
        inst.collisionFilterInfo = d["collisionFilterInfo"]

        return inst
