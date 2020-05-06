from ..binary import BinaryReader, BinaryWriter
from .base import HKBaseClass
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
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkpRigidBody(HKBaseClass, hkpEntity):
    def __init__(self):
        hkpEntity.__init__(self)

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        HKBaseClass.deserialize(self, hkFile, br, obj)
        hkpEntity.deserialize(self, hkFile, br, obj)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        HKBaseClass.assign_class(self, hkFile, obj)
        hkpEntity.serialize(self, hkFile, bw, obj)

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def as_dict(self):
        d = HKBaseClass.as_dict(self)
        d.update(hkpEntity.as_dict(self))
        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBaseClass.from_dict(d).__dict__)
        inst.__dict__.update(hkpEntity.from_dict(d).__dict__)
        return inst
