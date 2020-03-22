import io
from typing import Union

from .binary import BinaryReader, BinaryWriter
from .container import HKClassnamesSection, HKDataSection, HKHeader, HKTypesSection


class HK:
    header: HKHeader

    classnames: HKClassnamesSection
    types: HKTypesSection
    data: HKDataSection

    def __init__(self):
        self.classnames = HKClassnamesSection()
        self.types = HKTypesSection()
        self.data = HKDataSection()

    def read(self, br: BinaryReader):
        # Read the endian byte ahead
        br.step_in(0x11)
        br.big_endian = br.read_int8() == 0
        br.step_out()

        # Create all needed instances
        self.header = HKHeader()
        self.classnames = HKClassnamesSection()
        self.types = HKTypesSection()
        self.data = HKDataSection()

        # Read Havok header
        self.header.read(br)

        # Read Havok sections' headers
        self.classnames.read_header(br)
        self.types.read_header(br)
        self.data.read_header(br)

        # Read Havok sections' data
        self.classnames.read(br)
        self.types.read(br)
        self.data.read(self, br)

    def write(self, bw: BinaryWriter):        
        # Write Havok header
        self.header.write(bw)

        # Write Havok sections' header
        self.classnames.write_header(bw)
        self.types.write_header(bw)
        self.data.write_header(bw)

        # Write Havok sections' data
        self.classnames.write(bw)
        self.types.write(bw)
        self.data.write(self, bw)

    def deserialize(self):
        self.data.deserialize(self)

    def serialize(self):
        self.data.serialize(self)

    def _assert_pointer(self, br: BinaryReader):
        if self.header.pointer_size == 4:
            br.assert_int32(0)
        elif self.header.pointer_size == 8:
            br.assert_int64(0)
        else:
            raise NotImplementedError("Wrong pointer size!")

    def _write_empty_pointer(self, bw: BinaryWriter):
        if self.header.pointer_size == 4:
            bw.write_int32(0)
        elif self.header.pointer_size == 8:
            bw.write_int64(0)
        else:
            raise Exception("Wrong pointer size!")

    def _read_counter(self, br: BinaryReader):
        self._assert_pointer(br)
        count = br.read_int32()  # 0x0000000X
        br.assert_uint32(0x80000000 | count)  # 0x8000000X
        return count

    def _write_counter(self, bw: BinaryWriter, count: int):
        self._write_empty_pointer(bw)
        bw.write_int32(count)
        bw.write_uint32(0x80000000 | count)

    def asdict(self):
        return {
            "header": self.header.asdict(),
            "data": self.data.asdict(),
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.header = HKHeader.fromdict(d["header"])
        inst.data = HKDataSection.fromdict(d["data"])

        return inst

    def to_switch(self):
        self.header.to_switch()

    def to_wiiu(self):
        self.header.to_wiiu()

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.header})>"
