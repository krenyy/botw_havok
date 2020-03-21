from ...binary import BinaryReader, BinaryWriter
from ..enums.ShapeDispatchTypeEnum import ShapeDispatchTypeEnum
from ..enums.ShapeInfoCodecTypeEnum import ShapeInfoCodecTypeEnum
from .hkReferencedObject import hkReferencedObject

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
                "dispatchType": ShapeDispatchTypeEnum(self.dispatchType).name,
                "bitsPerKey": self.bitsPerKey,
                "shapeInfoCodecType": ShapeInfoCodecTypeEnum(
                    self.shapeInfoCodecType
                ).name,
            }
        )

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.type = d["type"]
        inst.dispatchType = ShapeDispatchTypeEnum[d["dispatchType"]].value
        inst.bitsPerKey = d["bitsPerKey"]
        inst.shapeInfoCodecType = ShapeInfoCodecTypeEnum[d["shapeInfoCodecType"]].value

        return inst
