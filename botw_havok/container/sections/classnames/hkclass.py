from typing import TYPE_CHECKING

from ....binary import BinaryReader, BinaryWriter
from ....binary.types import UInt32
from ....classes.util.signature_map import HKSignatureMap

if TYPE_CHECKING:
    from .hkclassnamessection import HKClassnamesSection


class HKClass:
    signature: UInt32
    name: str
    offset: UInt32

    def read(self, csec: "HKClassnamesSection", br: BinaryReader):
        self.signature = br.read_uint32()
        br.assert_int8(0x09)  # Delimiter between class name and signature
        self.offset = br.tell() - csec.absolute_offset
        self.name = br.read_string()

    def write(self, csec: "HKClassnamesSection", bw: BinaryWriter):
        bw.write_uint32(self.signature)
        bw.write_int8(0x09)
        self.offset = bw.tell() - csec.absolute_offset
        bw.write_string(self.name)

    @classmethod
    def from_name(cls, name: str):
        inst = cls()
        inst.name = name
        inst.signature = HKSignatureMap.get(name)

        return inst

    def __repr__(self):
        return f"<{self.name}({self.offset})>"
