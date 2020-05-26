from typing import TYPE_CHECKING

from .hkpShape import hkpShape
from ..enums.BvTreeType import BvTreeType
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt8

if TYPE_CHECKING:
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

    def as_dict(self):
        d = super().as_dict()
        d.update({"bvTreeType": BvTreeType(self.bvTreeType).name})

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().from_dict(d).__dict__)

        inst.bvTreeType = BvTreeType[d["bvTreeType"]].value

        return inst
