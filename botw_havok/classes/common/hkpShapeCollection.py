from typing import TYPE_CHECKING

from .hkpShape import hkpShape
from ..enums.CollectionType import CollectionType
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt8

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpShapeCollection(hkpShape):
    disableWelding: bool
    collectionType: UInt8

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        br.align_to(16)

        self.disableWelding = bool(br.read_uint8())
        self.collectionType = br.read_uint8()

        br.align_to(8)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        bw.align_to(16)

        bw.write_uint8(UInt8(self.disableWelding))
        bw.write_uint8(self.collectionType)

        bw.align_to(8)

    def as_dict(self):
        d = super().as_dict()
        d.update(
            {
                "disableWelding": self.disableWelding,
                "collectionType": CollectionType(self.collectionType),
            }
        )
        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().from_dict(d).__dict__)

        inst.disableWelding = d["disableWelding"]
        inst.collectionType = CollectionType[d["collectionType"]]

        return inst
