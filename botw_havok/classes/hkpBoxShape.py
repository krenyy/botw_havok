from ..binary import BinaryReader, BinaryWriter
from ..util import Vector4
from .base import HKBase
from .common.hkpConvexShape import hkpConvexShape

if False:
    from ..hk import HK


class hkpBoxShape(HKBase, hkpConvexShape):
    halfExtents: Vector4

    def deserialize(self, hk: "HK", obj):
        HKBase.deserialize(self, hk, obj)

        br = BinaryReader(self.hkobj.bytes)
        br.big_endian = hk.header.endian == 0

        hkpConvexShape.deserialize(self, hk, br, obj)

        self.halfExtents = br.read_vector4()

    def serialize(self, hk: "HK"):
        HKBase.assign_class(self, hk)

        bw = BinaryWriter()
        bw.big_endian = hk.header.endian == 0

        hkpConvexShape.serialize(self, hk, bw, self.hkobj)

        bw.write_vector4(self.halfExtents)

    def asdict(self):
        d = super().asdict()
        d.update({"halfExtents": self.halfExtents})

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.halfExtents = d["halfExtents"]

        return inst
