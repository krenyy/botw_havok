from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpBroadPhaseHandle(hkObject):
    id: UInt32

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.id = br.read_uint32()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_uint32(UInt32(self.id))

    def as_dict(self):
        return {"id": self.id}

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()

        inst.id = d["id"]

        return inst
