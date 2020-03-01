from ...binary import BinaryReader, BinaryWriter
from .hkpSphereRepShape import hkpSphereRepShape


class hkpConvexShape(hkpSphereRepShape):
    radius: float

    def deserialize(self, hk, br: BinaryReader, obj):
        self.radius = br.read_single()
        br.align_to(16)  # TODO: Check if correct

    def serialize(self, hk, bw: BinaryWriter, obj):
        bw.write_single(self.radius)
        bw.align_to(16)

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
