import typing

from ...binary import BinaryReader, BinaryWriter
from .util import GlobalFixup, LocalFixup, GlobalReference


class HKSection:
    id: int  # 0,1,2
    tag: str  # __classnames__, __types__, __data__

    local_fixups: typing.List[LocalFixup]
    global_fixups: typing.List[GlobalFixup]
    virtual_fixups: typing.List[GlobalFixup]

    absolute_offset: int  # Used in each section, defines absolute section start
    local_fixups_offset: int  # Used in the data section, points to local links
    global_fixups_offset: int  # Used in the data section, points to global links
    virtual_fixups_offset: int  # Used in the data section, links chunks to classes
    exports_offset: int  # Never used?, equals to EOF_offset
    imports_offset: int  # Never used?, equals to EOF_offset
    EOF_offset: int  # Points to the end of the section

    def __init__(self):
        self.local_fixups = []
        self.global_fixups = []
        self.virtual_fixups = []

    def read_header(self, br: BinaryReader):
        # Section name
        self.tag = br.read_string(19)
        br.assert_uint8(0xFF)

        # Section offsets
        self.absolute_offset = br.read_uint32()
        self.local_fixups_offset = br.read_uint32()
        self.global_fixups_offset = br.read_uint32()
        self.virtual_fixups_offset = br.read_uint32()
        self.exports_offset = br.read_uint32()
        self.imports_offset = br.read_uint32()
        self.EOF_offset = br.read_uint32()

        # Delimiter between section headers
        br.assert_uint32(0xFFFFFFFF)
        br.assert_uint32(0xFFFFFFFF)
        br.assert_uint32(0xFFFFFFFF)
        br.assert_uint32(0xFFFFFFFF)

    def write_header(self, bw: BinaryWriter):
        # Section name
        bw.write_string(self.tag, size=19)
        bw.write_uint8(0xFF)

        # Section offsets
        bw.reserve_uint32(f"{self.tag}abs")
        bw.reserve_uint32(f"{self.tag}loc")
        bw.reserve_uint32(f"{self.tag}glob")
        bw.reserve_uint32(f"{self.tag}virt")
        bw.reserve_uint32(f"{self.tag}exp")
        bw.reserve_uint32(f"{self.tag}imp")
        bw.reserve_uint32(f"{self.tag}eof")

        # Delimiter between section headers
        bw.write_uint32(0xFFFFFFFF)
        bw.write_uint32(0xFFFFFFFF)
        bw.write_uint32(0xFFFFFFFF)
        bw.write_uint32(0xFFFFFFFF)

    def read(self, br: BinaryReader):
        # Read data links
        br.step_in(self.absolute_offset + self.local_fixups_offset)
        self.local_fixups = self._read_local_fixups(
            br, self.global_fixups_offset - self.local_fixups_offset
        )
        br.step_out()

        # Read chunk links
        br.step_in(self.absolute_offset + self.global_fixups_offset)
        self.global_fixups = self._read_global_fixups(
            br, self.virtual_fixups_offset - self.global_fixups_offset
        )
        br.step_out()

        # Read class mappings
        br.step_in(self.absolute_offset + self.virtual_fixups_offset)
        self.virtual_fixups = self._read_global_fixups(
            br, self.exports_offset - self.virtual_fixups_offset
        )
        br.step_out()

    def _read_local_fixups(self, br: BinaryReader, length: int):
        ret = []
        for _ in range(length // 8):
            if br.peek() != b"\xFF":
                lfu = LocalFixup()
                lfu.read(br)
                ret.append(lfu)
        br.align_to(16)
        return ret

    def _read_global_fixups(self, br: BinaryReader, length: int):
        ret = []
        for _ in range(length // 12):
            if br.peek() != b"\xFF":
                gfu = GlobalFixup()
                gfu.read(br)
                ret.append(gfu)
        br.align_to(16)
        return ret

    def asdict(self):
        raise NotImplementedError("This method is meant to be overridden!")

    def fromdict(self, d: dict):
        raise NotImplementedError("This method is meant to be overridden!")
