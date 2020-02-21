from ...binary import BinaryReader, BinaryWriter
from ..enums.SpuCollisionCallbackEventFilter import SpuCollisionCallbackEventFilter

if False:
    from ...hk import HK


class hkpEntitySpuCollisionCallback:
    # util: None = None

    capacity: int
    eventFilter: int
    userFilter: int

    def deserialize(self, hk: "HK", br: BinaryReader):
        util_offset = br.tell()
        hk._assert_pointer(br)  # util pointer

        self.capacity = br.read_uint16()
        self.eventFilter = br.read_uint8()
        self.userFilter = br.read_uint8()

        if hk.header.padding_option:
            br.read_uint32()

    def serialize(self, hk: "HK", bw: BinaryWriter):
        util_offset = bw.tell()
        hk._write_empty_pointer(bw)

        bw.write_uint16(self.capacity)
        bw.write_uint8(self.eventFilter)
        bw.write_uint8(self.userFilter)

        if hk.header.padding_option:
            bw.write_uint32(0x0)

    def asdict(self):
        return {
            # "util": self.util,
            "capacity": self.capacity,
            "eventFilter": SpuCollisionCallbackEventFilter(self.eventFilter).name,
            "userFilter": SpuCollisionCallbackEventFilter(self.userFilter).name,
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        # inst.util = d["util"]
        inst.capacity = d["capacity"]
        inst.eventFilter = SpuCollisionCallbackEventFilter[d["eventFilter"]].value
        inst.userFilter = SpuCollisionCallbackEventFilter[d["userFilter"]].value

        return inst
