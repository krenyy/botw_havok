from ..binary import BinaryReader, BinaryWriter
from ..util import Vector4
from .base import HKBase
from .common.hkpConvexShape import hkpConvexShape

if False:
    from ..hk import HK


class hkpCylinderShape(HKBase, hkpConvexShape):
    cylRadius: float
    cylBaseRadiusFactorForHeightFieldCollisions: float

    vertexA: Vector4
    vertexB: Vector4

    perpendicular1: Vector4
    perpendicular2: Vector4

    def deserialize(self, hk: "HK", obj):
        HKBase.deserialize(self, hk, obj)

        br = BinaryReader(self.hkobj.bytes)
        br.big_endian = hk.header.endian == 0

        hkpConvexShape.deserialize(self, hk, br, obj)

        self.cylRadius = br.read_single()
        self.cylBaseRadiusFactorForHeightFieldCollisions = br.read_single()

        self.vertexA = br.read_vector4()
        self.vertexB = br.read_vector4()

        self.perpendicular1 = br.read_vector4()
        self.perpendicular2 = br.read_vector4()

        br.align_to(16)

    def serialize(self, hk: "HK"):
        HKBase.assign_class(self, hk)

        bw = BinaryWriter()
        bw.big_endian = hk.header.endian == 0

        hkpConvexShape.serialize(self, hk, bw, self.hkobj)

        bw.write_single(self.cylRadius)
        bw.write_single(self.cylBaseRadiusFactorForHeightFieldCollisions)

        bw.write_vector4(self.vertexA)
        bw.write_vector4(self.vertexB)

        bw.write_vector4(self.perpendicular1)
        bw.write_vector4(self.perpendicular2)

        bw.align_to(16)

        HKBase.serialize(self, hk, bw)

    def asdict(self):
        d = HKBase.asdict(self)
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
        inst.__dict__.update(HKBase.fromdict(d).__dict__)
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
