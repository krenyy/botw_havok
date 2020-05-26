from typing import TYPE_CHECKING
from typing import Union

from .hkpShapeBase import hkpShapeBase
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32, UInt64

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpShape(hkpShapeBase):
    userData: Union[UInt32, UInt64]

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        if hkFile.header.pointer_size == 8:
            self.userData = br.read_uint64()
        elif hkFile.header.pointer_size == 4:
            self.userData = br.read_uint32()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        if hkFile.header.pointer_size == 8:
            bw.write_uint64(UInt64(self.userData))
        elif hkFile.header.pointer_size == 4:
            bw.write_uint32(UInt32(self.userData))

    def as_dict(self):
        d = super().as_dict()
        d.update({"userData": self.userData})
        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().from_dict(d).__dict__)

        inst.userData = d["userData"]

        return inst
