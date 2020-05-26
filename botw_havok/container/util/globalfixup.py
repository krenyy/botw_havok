from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Int32, UInt32


class GlobalFixup:
    src: UInt32
    dst_section_id: Int32
    dst: UInt32

    def read(self, br: BinaryReader):
        self.src = br.read_uint32()
        self.dst_section_id = br.read_int32()
        self.dst = br.read_uint32()

    def write(self, bw: BinaryWriter):
        bw.write_uint32(self.src)
        bw.write_int32(self.dst_section_id)
        bw.write_uint32(self.dst)

    def __eq__(self, value: object):
        if not isinstance(value, GlobalFixup):
            raise NotImplementedError()
        return (
                (self.src == value.src)
                and (self.dst_section_id == value.dst_section_id)
                and (self.dst == value.dst)
        )

    def __hash__(self):
        return hash((self.src, self.dst_section_id, self.dst))

    def __repr__(self):
        return f"{self.__class__.__name__}({hex(self.src)}, {hex(self.dst)})"
