from typing import TYPE_CHECKING

from .hkObject import hkObject
from ..enums.SpuCollisionCallbackEventFilter import SpuCollisionCallbackEventFilter
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt8, UInt16, UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpEntitySpuCollisionCallback(hkObject):
    # util: None = None

    capacity: UInt16
    eventFilter: UInt8
    userFilter: UInt8

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        hkFile._assert_pointer(br)  # empty 'util' pointer

        self.capacity = br.read_uint16()
        self.eventFilter = br.read_uint8()
        self.userFilter = br.read_uint8()

        if hkFile.header.padding_option:
            br.read_uint32()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        hkFile._write_empty_pointer(bw)  # empty 'util' pointer

        bw.write_uint16(UInt16(self.capacity))
        bw.write_uint8(UInt8(self.eventFilter))
        bw.write_uint8(UInt8(self.userFilter))

        if hkFile.header.padding_option:
            bw.write_uint32(UInt32(0))

    def as_dict(self):
        return {
            # "util": self.util,
            "capacity": self.capacity,
            "eventFilter": SpuCollisionCallbackEventFilter(self.eventFilter).name,
            "userFilter": SpuCollisionCallbackEventFilter(self.userFilter).name,
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        # inst.util = d["util"]
        inst.capacity = d["capacity"]
        inst.eventFilter = SpuCollisionCallbackEventFilter[d["eventFilter"]].value
        inst.userFilter = SpuCollisionCallbackEventFilter[d["userFilter"]].value

        return inst
