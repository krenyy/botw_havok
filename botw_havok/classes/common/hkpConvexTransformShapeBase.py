from typing import TYPE_CHECKING

from .hkpConvexShape import hkpConvexShape
from .hkpSingleShapeContainer import hkpSingleShapeContainer
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Int32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpConvexTransformShapeBase(hkpConvexShape):
    childShape: hkpSingleShapeContainer
    childShapeSizeForSpu: Int32

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        if hkFile.header.padding_option:
            br.align_to(8)

        self.childShape = hkpSingleShapeContainer()
        self.childShape.deserialize(hkFile, br, obj)

        self.childShapeSizeForSpu = br.read_int32()

        br.align_to(8)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        if hkFile.header.padding_option:
            bw.align_to(8)

        self.childShape.serialize(hkFile, bw, obj)

        bw.write_int32(self.childShapeSizeForSpu)

        bw.align_to(8)

    def as_dict(self):
        d = super().as_dict()
        d.update(
            {
                "childShape": self.childShape.as_dict(),
                "childShapeSizeForSpu": self.childShapeSizeForSpu,
            }
        )
        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().from_dict(d))
        inst.__dict__.update(
            {
                "childShape": hkpSingleShapeContainer.from_dict(d["childShape"]),
                "childShapeSizeForSpu": d["childShapeSizeForSpu"],
            }
        )

        return inst
