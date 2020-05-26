from typing import TYPE_CHECKING

from .hkcdStaticTreeCodec3Axis import hkcdStaticTreeCodec3Axis
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt8

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkcdStaticTreeCodec3Axis5(hkcdStaticTreeCodec3Axis):
    hiData: UInt8
    loData: UInt8

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        self.hiData = br.read_uint8()
        self.loData = br.read_uint8()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        bw.write_uint8(UInt8(self.hiData))
        bw.write_uint8(UInt8(self.loData))

    def as_dict(self):
        d = super().as_dict()
        d.update({"hiData": self.hiData, "loData": self.loData})
        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().from_dict(d).__dict__)

        inst.hiData = d["hiData"]
        inst.loData = d["loData"]

        return inst
