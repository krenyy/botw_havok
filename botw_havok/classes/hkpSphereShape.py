from typing import Sequence
from typing import TYPE_CHECKING

from .base import HKBaseClass
from .common.hkpConvexShape import hkpConvexShape
from ..binary import BinaryReader, BinaryWriter
from ..binary.types import UInt32

if TYPE_CHECKING:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkpSphereShape(HKBaseClass, hkpConvexShape):
    pad16: Sequence[UInt32]

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        HKBaseClass.deserialize(self, hkFile, br, obj)
        hkpConvexShape.deserialize(self, hkFile, br, obj)

        self.pad16 = [br.read_uint32() for _ in range(3)]

        br.align_to(16)  # what the heck

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        HKBaseClass.assign_class(self, hkFile, obj)
        hkpConvexShape.serialize(self, hkFile, bw, obj)

        ###

        [bw.write_uint32(i) for i in self.pad16]

        bw.align_to(16)

        ###

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def as_dict(self):
        d = HKBaseClass.as_dict(self)
        d.update(hkpConvexShape.as_dict(self))

        d.update({"pad16": self.pad16})

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBaseClass.from_dict(d).__dict__)
        inst.__dict__.update(hkpConvexShape.from_dict(d).__dict__)

        inst.pad16 = d["pad16"]

        return inst
