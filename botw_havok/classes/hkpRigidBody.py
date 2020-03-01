from ..binary import BinaryReader, BinaryWriter
from .base import HKBase
from .common.hkMultiThreadCheck import hkMultiThreadCheck
from .common.hkpConstraintInstance import hkpConstraintInstance
from .common.hkpEntity import hkpEntity
from .common.hkpEntitySmallArraySerializeOverrideType import (
    hkpEntitySmallArraySerializeOverrideType,
)
from .common.hkpEntitySpuCollisionCallback import hkpEntitySpuCollisionCallback
from .common.hkpLinkedCollidable import hkpLinkedCollidable
from .common.hkpMaterial import hkpMaterial
from .common.hkpMaxSizeMotion import hkpMaxSizeMotion

if False:
    from ..hk import HK
    from ..container.sections.hkobject import HKObject


class hkpRigidBody(HKBase, hkpEntity):
    def deserialize(self, hk: "HK", obj: "HKObject"):
        HKBase.deserialize(self, hk, obj)

        br = BinaryReader(obj.bytes)
        br.big_endian = hk.header.endian == 0

        hkpEntity.deserialize(self, hk, br, obj)

    def serialize(self, hk: "HK"):
        HKBase.assign_class(self, hk)

        bw = BinaryWriter()
        bw.big_endian = hk.header.endian == 0

        hkpEntity.serialize(self, hk, bw, self.hkobj)

        HKBase.serialize(self, hk, bw)

    def asdict(self):
        d = HKBase.asdict(self)
        d.update(hkpEntity.asdict(self))
        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBase.fromdict(d).__dict__)
        inst.__dict__.update(hkpEntity.fromdict(d).__dict__)
        return inst
