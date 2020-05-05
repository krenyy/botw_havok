from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt8
from ..enums.BvTreeType import BvTreeType
from .hkpShape import hkpShape

if False:
    from ...container.util.hkobject import HKObject


class hkpBvTreeShape(hkpShape):
    bvTreeType: UInt8

    def deserialize(self, hkFile, br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        self.bvTreeType = br.read_uint8()
        br.align_to(4)

    def serialize(self, hkFile, bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        bw.write_uint8(UInt8(self.bvTreeType))
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
