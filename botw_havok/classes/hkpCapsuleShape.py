from typing import TYPE_CHECKING

from .base import HKBaseClass
from .common.hkpConvexShape import hkpConvexShape
from ..binary import BinaryReader, BinaryWriter
from ..binary.types import Vector4

if TYPE_CHECKING:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkpCapsuleShape(HKBaseClass, hkpConvexShape):
    vertexA: Vector4
    vertexB: Vector4

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        HKBaseClass.deserialize(self, hkFile, br, obj)
        hkpConvexShape.deserialize(self, hkFile, br, obj)

        ###

        br.align_to(16)

        self.vertexA = br.read_vector4()
        self.vertexB = br.read_vector4()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        HKBaseClass.assign_class(self, hkFile, obj)
        hkpConvexShape.serialize(self, hkFile, bw, obj)

        ###

        bw.align_to(16)

        bw.write_vector(self.vertexA)
        bw.write_vector(self.vertexB)

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def as_dict(self):
        d = HKBaseClass.as_dict(self)
        d.update(hkpConvexShape.as_dict(self))
        d.update({"vertexA": self.vertexA.as_dict(), "vertexB": self.vertexB.as_dict()})

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBaseClass.from_dict(d).__dict__)
        inst.__dict__.update(hkpConvexShape.from_dict(d).__dict__)

        inst.vertexA = Vector4.from_dict(d["vertexA"])
        inst.vertexB = Vector4.from_dict(d["vertexB"])

        return inst
