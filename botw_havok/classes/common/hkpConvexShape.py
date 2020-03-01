from ...binary import BinaryReader, BinaryWriter
from .hkpSphereRepShape import hkpSphereRepShape


class hkpConvexShape(hkpSphereRepShape):
    radius: float

    def deserialize(self, hk, br: BinaryReader, obj):
        super().deserialize(hk, br)

        self.radius = br.read_single()

    def serialize(self, hk, bw: BinaryWriter, obj):
        super().serialize(hk, bw)

        bw.write_single(self.radius)

    def asdict(self):
        d = super().asdict()
        d.update({"radius": self.radius})

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.radius = d["radius"]

        return inst
