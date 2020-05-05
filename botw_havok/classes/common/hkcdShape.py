from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt8
from ..enums.ShapeDispatchTypeEnum import ShapeDispatchTypeEnum
from ..enums.ShapeInfoCodecTypeEnum import ShapeInfoCodecTypeEnum
from .hkReferencedObject import hkReferencedObject

if False:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkcdShape(hkReferencedObject):
    type: UInt8
    dispatchType: UInt8
    bitsPerKey: UInt8
    shapeInfoCodecType: UInt8

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        self.type = br.read_uint8()
        self.dispatchType = br.read_uint8()
        self.bitsPerKey = br.read_uint8()
        self.shapeInfoCodecType = br.read_uint8()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        bw.write_uint8(UInt8(self.type))
        bw.write_uint8(UInt8(self.dispatchType))
        bw.write_uint8(UInt8(self.bitsPerKey))
        bw.write_uint8(UInt8(self.shapeInfoCodecType))

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
