from typing import TYPE_CHECKING

from .base import HKBaseClass
from .common.hkpConvexTransformShapeBase import hkpConvexTransformShapeBase
from ..binary import BinaryReader, BinaryWriter
from ..binary.types import Matrix, Vector4

if TYPE_CHECKING:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkpConvexTransformShape(HKBaseClass, hkpConvexTransformShapeBase):
    transform: Matrix
    extraScale: Vector4

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        HKBaseClass.deserialize(self, hkFile, br, obj)
        hkpConvexTransformShapeBase.deserialize(self, hkFile, br, obj)

        ###

        self.transform = br.read_matrix(3)
        self.extraScale = br.read_vector4()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        HKBaseClass.assign_class(self, hkFile, obj)
        hkpConvexTransformShapeBase.serialize(self, hkFile, bw, obj)

        ###

        bw.write_matrix(self.transform)
        bw.write_vector(self.extraScale)

        ###

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def as_dict(self):
        d = hkpConvexTransformShapeBase.as_dict(self)
        d.update(
            {
                "transform": self.transform.as_dict(),
                "extraScale": self.extraScale.as_dict(),
            }
        )
        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(hkpConvexTransformShapeBase.from_dict(d).__dict__)
        inst.__dict__.update(
            {
                "transform": Matrix.from_dict(d["transform"]),
                "extraScale": Vector4.from_dict(d["extraScale"]),
            }
        )

        return inst
