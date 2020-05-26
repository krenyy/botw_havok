from typing import TYPE_CHECKING

from .hkpSphereRepShape import hkpSphereRepShape
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Float32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpConvexShape(hkpSphereRepShape):
    radius: Float32

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        self.radius = br.read_float32()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        bw.write_float32(Float32(self.radius))

    def as_dict(self):
        d = super().as_dict()
        d.update({"radius": self.radius})

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().from_dict(d).__dict__)

        inst.radius = Float32(d["radius"])

        return inst
