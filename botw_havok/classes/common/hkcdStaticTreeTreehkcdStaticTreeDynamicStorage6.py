from typing import TYPE_CHECKING

from .hkAabb import hkAabb
from .hkcdStaticTreeDynamicStorage6 import hkcdStaticTreeDynamicStorage6
from ...binary import BinaryReader, BinaryWriter

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkcdStaticTreeTreehkcdStaticTreeDynamicStorage6(hkcdStaticTreeDynamicStorage6):
    domain: hkAabb

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        self.domain = hkAabb()
        self.domain.deserialize(hkFile, br, obj)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        self.domain.serialize(hkFile, bw, obj)

    def as_dict(self):
        d = super().as_dict()
        d.update({"domain": self.domain.as_dict()})

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().from_dict(d).__dict__)

        inst.domain = hkAabb.from_dict(d["domain"])

        return inst
