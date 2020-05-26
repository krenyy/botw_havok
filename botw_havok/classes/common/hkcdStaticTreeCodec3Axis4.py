from typing import TYPE_CHECKING

from .hkcdStaticTreeCodec3Axis import hkcdStaticTreeCodec3Axis
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt8

if TYPE_CHECKING:
    from ...container.util.hkobject import HKObject


class hkcdStaticTreeCodec3Axis4(hkcdStaticTreeCodec3Axis):
    data: UInt8

    def deserialize(self, hkFile, br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        self.data = br.read_uint8()

    def serialize(self, hkFile, bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        bw.write_uint8(UInt8(self.data))

    def as_dict(self):
        d = super().as_dict()
        d.update({"data": self.data})
        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().from_dict(d).__dict__)

        inst.data = d["data"]

        return inst
