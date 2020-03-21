from ...binary import BinaryReader, BinaryWriter
from ...container.sections.hkobject import HKObject
from .hkcdStaticTreeCodec3Axis import hkcdStaticTreeCodec3Axis

if False:
    from ...hk import HK


class hkcdStaticTreeCodec3Axis6(hkcdStaticTreeCodec3Axis):
    hiData: int
    loData: int

    def deserialize(self, hk: "HK", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hk, br, obj)

        self.hiData = br.read_uint8()
        self.loData = br.read_uint16()

    def serialize(self, hk: "HK", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hk, bw, obj)

        bw.write_uint8(self.hiData)
        bw.write_uint16(self.loData)

    def asdict(self):
        d = super().asdict()
        d.update(
            {"hiData": self.hiData, "loData": self.loData,}
        )
        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.hiData = d["hiData"]
        inst.loData = d["loData"]

        return inst
