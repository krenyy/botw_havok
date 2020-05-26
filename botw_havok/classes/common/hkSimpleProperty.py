from typing import TYPE_CHECKING

from .hkObject import hkObject
from .hkSimplePropertyValue import hkSimplePropertyValue
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkSimpleProperty(hkObject):
    key: UInt32
    value: hkSimplePropertyValue

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.key = br.read_uint32()

        if hkFile.header.padding_option:
            br.read_uint32()

        self.value = hkSimplePropertyValue()
        self.value.deserialize(hkFile, br, obj)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_uint32(UInt32(self.key))

        if hkFile.header.padding_option:
            bw.write_uint32(UInt32(0x0))

        self.value.serialize(hkFile, bw, obj)

    def as_dict(self):
        return {"key": self.key, "value": self.value.as_dict()}

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.key = d["key"]
        inst.value = hkSimplePropertyValue.from_dict(d["value"])

        return inst
