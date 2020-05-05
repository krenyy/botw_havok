from ..binary import BinaryReader, BinaryWriter
from ..binary.types import Vector4
from .base import HKBaseClass
from .common.hkpConvexShape import hkpConvexShape

if False:
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

        bw.write_vector4(self.vertexA)
        bw.write_vector4(self.vertexB)

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def asdict(self):
        d = HKBaseClass.asdict(self)
        d.update(hkpConvexShape.asdict(self))
        d.update({"vertexA": self.vertexA.asdict(), "vertexB": self.vertexB.asdict()})

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBaseClass.fromdict(d).__dict__)
        inst.__dict__.update(hkpConvexShape.fromdict(d).__dict__)

        inst.vertexA = Vector4.fromdict(d["vertexA"])
        inst.vertexB = Vector4.fromdict(d["vertexB"])

        return inst
