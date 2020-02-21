from ...binary import BinaryReader, BinaryWriter
from .hkpShape import hkpShape
from ..enums.BvTreeType import BvTreeType


class hkpBvTreeShape(hkpShape):
    bvTreeType: int

    def deserialize(self, hk, br: BinaryReader, obj):
        super().deserialize(hk, br)

        self.bvTreeType = br.read_uint8()
        br.align_to(4)

    def serialize(self, hk, bw: BinaryWriter):
        super().serialize(hk, bw)

        bw.write_uint8(self.bvTreeType)
        bw.align_to(4)

    def asdict(self):
        d = super().asdict()
        d.update({"bvTreeType": BvTreeType(self.bvTreeType).name})

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.bvTreeType = BvTreeType[d["bvTreeType"]].value

        return inst
