from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt8
from .hkcdStaticTreeCodec3Axis import hkcdStaticTreeCodec3Axis

if False:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkcdStaticTreeCodec3Axis4(hkcdStaticTreeCodec3Axis):
    data: UInt8

    def deserialize(self, hkFile, br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        self.data = br.read_uint8()

    def serialize(self, hkFile, bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        bw.write_uint8(UInt8(self.data))

    def asdict(self):
        d = super().asdict()
        d.update({"data": self.data})
        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.data = d["data"]

        return inst
