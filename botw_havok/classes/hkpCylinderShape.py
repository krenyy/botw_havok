from ..binary import BinaryReader, BinaryWriter
from ..binary.types import Float32, Vector4
from .base import HKBaseClass
from .common.hkpConvexShape import hkpConvexShape

if False:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkpCylinderShape(HKBaseClass, hkpConvexShape):
    cylRadius: Float32
    cylBaseRadiusFactorForHeightFieldCollisions: Float32

    vertexA: Vector4
    vertexB: Vector4

    perpendicular1: Vector4
    perpendicular2: Vector4

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        HKBaseClass.deserialize(self, hkFile, br, obj)
        hkpConvexShape.deserialize(self, hkFile, br, obj)

        ###

        self.cylRadius = br.read_float32()
        self.cylBaseRadiusFactorForHeightFieldCollisions = br.read_float32()

        self.vertexA = br.read_vector4()
        self.vertexB = br.read_vector4()

        self.perpendicular1 = br.read_vector4()
        self.perpendicular2 = br.read_vector4()

        br.align_to(16)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        HKBaseClass.assign_class(self, hkFile, obj)
        hkpConvexShape.serialize(self, hkFile, bw, obj)

        ###

        bw.write_float32(Float32(self.cylRadius))
        bw.write_float32(Float32(self.cylBaseRadiusFactorForHeightFieldCollisions))

        bw.write_vector4(self.vertexA)
        bw.write_vector4(self.vertexB)

        bw.write_vector4(self.perpendicular1)
        bw.write_vector4(self.perpendicular2)

        bw.align_to(16)

        ###

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def asdict(self):
        d = HKBaseClass.asdict(self)
        d.update(hkpConvexShape.asdict(self))
        d.update(
            {
                "cylRadius": self.cylRadius,
                "cylBaseRadiusFactorForHeightFieldCollisions": self.cylBaseRadiusFactorForHeightFieldCollisions,
                "vertexA": self.vertexA.asdict(),
                "vertexB": self.vertexB.asdict(),
                "perpendicular1": self.perpendicular1.asdict(),
                "perpendicular2": self.perpendicular2.asdict(),
            }
        )

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBaseClass.fromdict(d).__dict__)
        inst.__dict__.update(hkpConvexShape.fromdict(d).__dict__)

        inst.cylRadius = d["cylRadius"]
        inst.cylBaseRadiusFactorForHeightFieldCollisions = d[
            "cylBaseRadiusFactorForHeightFieldCollisions"
        ]
        inst.vertexA = Vector4.fromdict(d["vertexA"])
        inst.vertexB = Vector4.fromdict(d["vertexB"])
        inst.perpendicular2 = Vector4.fromdict(d["perpendicular2"])
        inst.perpendicular1 = Vector4.fromdict(d["perpendicular1"])

        return inst
