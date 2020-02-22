from .hkAabb import hkAabb
from .hkcdStaticTreeDynamicStorage4 import hkcdStaticTreeDynamicStorage4


class hkcdStaticTreeTreehkcdStaticTreeDynamicStorage4(hkcdStaticTreeDynamicStorage4):
    domain: hkAabb

    def deserialize(self, hk, br, obj):
        super().deserialize(hk, br, obj)

        self.domain = hkAabb()
        self.domain.deserialize(hk, br)

    def serialize(self, hk, bw):
        super().serialize(hk, bw)

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
