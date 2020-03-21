from .hkpShapeBase import hkpShapeBase
from ...binary import BinaryReader, BinaryWriter

if False:
    from ...hk import HK


class hkpShape(hkpShapeBase):
    userData: int

    def deserialize(self, hk: "HK", br: BinaryReader):
        super().deserialize(hk, br)

        if hk.header.pointer_size == 8:
            self.userData = br.read_uint64()
        elif hk.header.pointer_size == 4:
            self.userData = br.read_uint32()

    def serialize(self, hk: "HK", bw: BinaryWriter):
        super().serialize(hk, bw)

        if hk.header.pointer_size == 8:
            bw.write_uint64(self.userData)
        elif hk.header.pointer_size == 4:
            bw.write_uint32(self.userData)

    def asdict(self):
        d = super().asdict()
        d.update({"userData": self.userData})
        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.userData = d["userData"]

        return inst
