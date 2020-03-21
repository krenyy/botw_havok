from ...binary import BinaryReader, BinaryWriter
from .hkAabb import hkAabb
from .hkcdStaticTreeDynamicStorage6 import hkcdStaticTreeDynamicStorage6

if False:
    from ...hk import HK
    from ...container.sections.hkobject import HKObject


class hkcdStaticTreeTreehkcdStaticTreeDynamicStorage6(hkcdStaticTreeDynamicStorage6):
    domain: hkAabb

    def deserialize(self, hk: "HK", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hk, br, obj)

        self.domain = hkAabb()
        self.domain.deserialize(hk, br)

    def serialize(self, hk: "HK", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hk, bw, obj)

        self.domain.serialize(hk, bw)

    def asdict(self):
        d = super().asdict()
        d.update({"domain": self.domain.asdict()})

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.domain = hkAabb.fromdict(d["domain"])

        return inst
