from .binary import BinaryReader, BinaryWriter
from .binary.types import Int32, Int64, UInt32
from .container import HKClassnamesSection, HKDataSection, HKHeader, HKTypesSection


class HKFile:
    header: HKHeader

    classnames: HKClassnamesSection
    types: HKTypesSection
    data: HKDataSection

    def __init__(self):
        self.header = HKHeader()

        self.classnames = HKClassnamesSection()
        self.types = HKTypesSection()
        self.data = HKDataSection()

    def read(self, br: BinaryReader):
        # Read the endian byte ahead
        br.step_in(0x11)
        br.big_endian = br.read_int8() == 0
        br.step_out()

        # Read Havok header
        self.header.read(br)

        # Read Havok sections' headers
        self.classnames.read_header(br)
        self.types.read_header(br)
        self.data.read_header(br)

        # Read Havok sections' data
        self.classnames.read(self, br)
        self.types.read(self, br)
        self.data.read(self, br)

    def write(self, bw: BinaryWriter):
        # Write Havok header
        self.header.write(bw)

        # Write Havok sections' header
        self.classnames.write_header(bw)
        self.types.write_header(bw)
        self.data.write_header(bw)

        # Write Havok sections' data
        self.classnames.write(self, bw)
        self.types.write(self, bw)
        self.data.write(self, bw)

    def deserialize(self) -> None:
        self.data.deserialize(self)

    def serialize(self) -> None:
        self.data.serialize(self)

    def to_switch(self):
        self.header.to_switch()

    def to_wiiu(self):
        self.header.to_wiiu()

    def _assert_pointer(self, br: BinaryReader) -> UInt32:
        offset = br.tell()
        if self.header.pointer_size == 4:
            br.assert_int32(Int32(0))
        elif self.header.pointer_size == 8:
            br.assert_int64(Int64(0))
        else:
            raise NotImplementedError("Wrong pointer size!")

        return offset

    def _write_empty_pointer(self, bw: BinaryWriter) -> UInt32:
        offset = bw.tell()
        if self.header.pointer_size == 4:
            bw.write_int32(Int32(0))
        elif self.header.pointer_size == 8:
            bw.write_int64(Int64(0))
        else:
            raise Exception("Wrong pointer size!")

        return offset

    def _read_counter(self, br: BinaryReader) -> UInt32:
        """Read Havok array size
        """
        count = br.read_uint32()
        br.assert_uint32(UInt32(0x80000000 | count))
        return count

    def _write_counter(self, bw: BinaryWriter, count: UInt32) -> None:
        bw.write_uint32(count)
        bw.write_uint32(UInt32(0x80000000 | count))

    def as_dict(self):
        return {
            "header": self.header.as_dict(),
            "data": self.data.as_dict(),
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.header = HKHeader.from_dict(d["header"])
        inst.data = HKDataSection.from_dict(d["data"])

        return inst

    def __repr__(self):
        return f"<{self.__class__.__name__}>"
