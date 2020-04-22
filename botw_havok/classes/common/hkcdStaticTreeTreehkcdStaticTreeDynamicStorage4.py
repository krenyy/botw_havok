from ...binary import BinaryReader, BinaryWriter
from .hkAabb import hkAabb
from .hkcdStaticTreeDynamicStorage4 import hkcdStaticTreeDynamicStorage4

if False:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkcdStaticTreeTreehkcdStaticTreeDynamicStorage4(hkcdStaticTreeDynamicStorage4):
    domain: hkAabb

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        self.domain = hkAabb()
        self.domain.deserialize(hkFile, br, obj)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        self.domain.serialize(hkFile, bw, obj)

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
