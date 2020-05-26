from typing import TYPE_CHECKING

from .base import HKBaseClass
from .common.hkpConvexShape import hkpConvexShape
from ..binary import BinaryReader, BinaryWriter
from ..binary.types import Vector4

if TYPE_CHECKING:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkpBoxShape(HKBaseClass, hkpConvexShape):
    halfExtents: Vector4

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        HKBaseClass.deserialize(self, hkFile, br, obj)
        hkpConvexShape.deserialize(self, hkFile, br, obj)

        ###

        br.align_to(16)

        self.halfExtents = br.read_vector4()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        HKBaseClass.assign_class(self, hkFile, obj)
        hkpConvexShape.serialize(self, hkFile, bw, obj)

        ###

        bw.align_to(16)

        bw.write_vector(self.halfExtents)

        ###

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def as_dict(self):
        d = HKBaseClass.as_dict(self)
        d.update(hkpConvexShape.as_dict(self))
        d.update({"halfExtents": self.halfExtents.as_dict()})

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBaseClass.from_dict(d).__dict__)
        inst.__dict__.update(hkpConvexShape.from_dict(d).__dict__)

        inst.halfExtents = Vector4.from_dict(d["halfExtents"])

        return inst
