from ...binary import BinaryReader, BinaryWriter
from .hkpBroadPhaseHandle import hkpBroadPhaseHandle

if False:
    from ...hk import HK


class hkpTypedBroadPhaseHandle(hkpBroadPhaseHandle):
    type: int
    ownerOffset: int
    objectQualityType: int
    collisionFilterInfo: int

    def deserialize(self, hk: "HK", br: BinaryReader):
        super().deserialize(hk, br)

        self.type = br.read_int8()
        self.ownerOffset = br.read_int8()
        self.objectQualityType = br.read_int8()
        br.align_to(4)

        self.collisionFilterInfo = br.read_uint32()

    def serialize(self, hk: "HK", bw: BinaryWriter):
        super().serialize(hk, bw)

        bw.write_int8(self.type)
        bw.write_int8(self.ownerOffset)
        bw.write_int8(self.objectQualityType)
        bw.align_to(4)

        bw.write_uint32(self.collisionFilterInfo)

    def asdict(self):
        d = super().asdict()
        d.update(
            {
                "type": self.type,
                "ownerOffset": self.ownerOffset,
                "objectQualityType": self.objectQualityType,
                "collisionFilterInfo": self.collisionFilterInfo,
            }
        )

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.id = d["id"]
        inst.type = d["type"]
        inst.ownerOffset = d["ownerOffset"]
        inst.objectQualityType = d["objectQualityType"]
        inst.collisionFilterInfo = d["collisionFilterInfo"]
