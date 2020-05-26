from typing import TYPE_CHECKING

from .base import HKBaseClass
from .common.hkpConvexTransformShapeBase import hkpConvexTransformShapeBase
from ..binary import BinaryReader, BinaryWriter
from ..binary.types import Vector4

if TYPE_CHECKING:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkpConvexTranslateShape(HKBaseClass, hkpConvexTransformShapeBase):
    translation: Vector4

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        HKBaseClass.deserialize(self, hkFile, br, obj)
        hkpConvexTransformShapeBase.deserialize(self, hkFile, br, obj)

        ###

        br.align_to(16)

        self.translation = br.read_vector4()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        HKBaseClass.assign_class(self, hkFile, obj)
        hkpConvexTransformShapeBase.serialize(self, hkFile, bw, obj)

        ###

        bw.align_to(16)

        bw.write_vector(self.translation)

        ###

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def as_dict(self):
        d = HKBaseClass.as_dict(self)
        d.update(hkpConvexTransformShapeBase.as_dict(self))
        d.update({"translation": self.translation})
        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBaseClass.from_dict(d).__dict__)
        inst.__dict__.update(hkpConvexTransformShapeBase.from_dict(d).__dict__)

        inst.translation = Vector4.from_dict(d["translation"])

        return inst
