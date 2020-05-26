from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt16, UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkMultiThreadCheck(hkObject):
    threadId: UInt32
    stackTraceId: UInt32
    markCount: UInt16
    markBitStack: UInt16

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.threadId = br.read_uint32()
        self.stackTraceId = br.read_uint32()
        self.markCount = br.read_uint16()
        self.markBitStack = br.read_uint16()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_uint32(UInt32(self.threadId))
        bw.write_uint32(UInt32(self.stackTraceId))
        bw.write_uint16(UInt16(self.markCount))
        bw.write_uint16(UInt16(self.markBitStack))

    def as_dict(self):
        return {
            "threadId": self.threadId,
            "stackTraceId": self.stackTraceId,
            "markCount": self.markCount,
            "markBitStack": self.markBitStack,
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.threadId = d["threadId"]
        inst.stackTraceId = d["stackTraceId"]
        inst.markCount = d["markCount"]
        inst.markBitStack = d["markBitStack"]

        return inst
