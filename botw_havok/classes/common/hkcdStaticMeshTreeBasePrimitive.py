from typing import List
from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt8

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkcdStaticMeshTreeBasePrimitive(hkObject):
    indices: List[UInt8]

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.indices = [br.read_uint8() for _ in range(4)]

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        [bw.write_uint8(UInt8(i)) for i in self.indices]

    def as_dict(self):
        return {"indices": self.indices}

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()

        inst.indices = d["indices"]

        return inst
