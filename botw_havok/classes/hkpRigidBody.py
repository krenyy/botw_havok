from ..binary import BinaryReader, BinaryWriter
from .base import HKBase
from .common.hkpEntity import hkpEntity

if False:
    from ..hk import HK
    from ..container.sections.hkobject import HKObject


class hkpRigidBody(HKBase, hkpEntity):
    def deserialize(self, hk: "HK", obj: "HKObject"):
        HKBase.deserialize(self, hk, obj)

        br = BinaryReader(obj.bytes)
        br.big_endian = hk.header.endian == 0

        hkpEntity.deserialize(self, hk, br, obj)

    def serialize(self, hk: "HK", bw: BinaryWriter):
        bw = BinaryWriter()
        bw.big_endian = hk.header.endian == 0

        hkpEntity.serialize(self, hk, bw)

        HKBase.serialize(self, hk, bw)

    def asdict(self):
        d = HKBase.asdict(self)
        d.update(hkpEntity.asdict(self))
        return d

    @classmethod
    def fromdict(cls, d: dict):
        pass
