from .hkAabb import hkAabb
from .hkcdStaticTreeDynamicStorage5 import hkcdStaticTreeDynamicStorage5


class hkcdStaticTreeTreehkcdStaticTreeDynamicStorage5(hkcdStaticTreeDynamicStorage5):
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
