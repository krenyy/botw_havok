from .hkReferencedObject import hkReferencedObject
from ...binary import BinaryReader, BinaryWriter

if False:
    from ...hk import HK


class hkcdShape(hkReferencedObject):
    type: int
    dispatchType: int
    bitsPerKey: int
    shapeInfoCodecType: int

    def deserialize(self, hk: "HK", br: BinaryReader):
        super().deserialize(hk, br)

        self.type = br.read_uint8()
        self.dispatchType = br.read_uint8()
        self.bitsPerKey = br.read_uint8()
        self.shapeInfoCodecType = br.read_uint8()

    def serialize(self, hk: "HK", bw: BinaryWriter):
        super().serialize(hk, bw)

        bw.write_uint8(self.type)
        bw.write_uint8(self.dispatchType)
        bw.write_uint8(self.bitsPerKey)
        bw.write_uint8(self.shapeInfoCodecType)

    def asdict(self):
        d = super().asdict()
        d.update(
            {
                "type": self.type,
                "dispatchType": self.dispatchType,
                "bitsPerKey": self.bitsPerKey,
                "shapeInfoCodecType": self.shapeInfoCodecType,
            }
        )

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.memSizeAndRefCount = d["memSizeAndRefCount"]
        inst.type = d["type"]
        inst.dispatchType = d["dispatchType"]
        inst.bitsPerKey = d["bitsPerKey"]
        inst.shapeInfoCodecType = d["shapeInfoCodecType"]

        return inst
