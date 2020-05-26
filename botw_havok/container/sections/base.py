import typing
from typing import TYPE_CHECKING

from ..util.globalfixup import GlobalFixup
from ..util.localfixup import LocalFixup
from ..util.virtualfixup import VirtualFixup
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt8, UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile


class HKSection:
    id: int  # 0,1,2
    tag: str  # __classnames__, __types__, __data__

    local_fixups: typing.List[LocalFixup]
    global_fixups: typing.List[GlobalFixup]
    virtual_fixups: typing.List[VirtualFixup]

    absolute_offset: UInt32  # Used in each section
    local_fixups_offset: UInt32  # Used in the data section
    global_fixups_offset: UInt32  # Used in the data section
    virtual_fixups_offset: UInt32  # Used in the data section
    exports_offset: UInt32  # Never used, equals to EOF_offset
    imports_offset: UInt32  # Never used, equals to EOF_offset
    EOF_offset: UInt32  # Points to the end of the section

    def __init__(self):
        self.local_fixups = []
        self.global_fixups = []
        self.virtual_fixups = []

    def read_header(self, br: BinaryReader):
        # Section name
        self.tag = br.read_string(19)
        br.assert_uint8(UInt8(0xFF))

        # Section offsets
        self.absolute_offset = br.read_uint32()
        self.local_fixups_offset = br.read_uint32()
        self.global_fixups_offset = br.read_uint32()
        self.virtual_fixups_offset = br.read_uint32()
        self.exports_offset = br.read_uint32()
        self.imports_offset = br.read_uint32()
        self.EOF_offset = br.read_uint32()

        # Delimiter between section headers
        br.assert_uint32(UInt32(0xFFFFFFFF))
        br.assert_uint32(UInt32(0xFFFFFFFF))
        br.assert_uint32(UInt32(0xFFFFFFFF))
        br.assert_uint32(UInt32(0xFFFFFFFF))

    def write_header(self, bw: BinaryWriter):
        # Section name
        bw.write_string(self.tag, size=19)
        bw.write_uint8(UInt8(0xFF))

        # Section offsets
        bw.reserve_uint32(f"{self.tag}abs")
        bw.reserve_uint32(f"{self.tag}loc")
        bw.reserve_uint32(f"{self.tag}glob")
        bw.reserve_uint32(f"{self.tag}virt")
        bw.reserve_uint32(f"{self.tag}exp")
        bw.reserve_uint32(f"{self.tag}imp")
        bw.reserve_uint32(f"{self.tag}eof")

        # Delimiter between section headers
        bw.write_uint32(UInt32(0xFFFFFFFF))
        bw.write_uint32(UInt32(0xFFFFFFFF))
        bw.write_uint32(UInt32(0xFFFFFFFF))
        bw.write_uint32(UInt32(0xFFFFFFFF))

    def read(self, hkFile: "HKFile", br: BinaryReader):
        ###
        # Read local fixups
        br.step_in(self.absolute_offset + self.local_fixups_offset)

        for _ in range((self.global_fixups_offset - self.local_fixups_offset) // 8):
            if br.peek() != b"\xFF":
                lfu = LocalFixup()
                lfu.read(br)

                self.local_fixups.append(lfu)

        br.step_out()

        ###
        # Read global fixups
        br.step_in(self.absolute_offset + self.global_fixups_offset)

        for _ in range((self.virtual_fixups_offset - self.global_fixups_offset) // 12):
            if br.peek() != b"\xFF":
                gfu = GlobalFixup()
                gfu.read(br)

                self.global_fixups.append(gfu)

        br.step_out()

        ###
        # Read virtual fixups
        br.step_in(self.absolute_offset + self.virtual_fixups_offset)

        for _ in range((self.exports_offset - self.virtual_fixups_offset) // 12):
            if br.peek() != b"\xFF":
                vfu = VirtualFixup()
                vfu.read(br)

                self.virtual_fixups.append(vfu)

        br.step_out()

    def write(self, hkFile: "HKFile", bw: BinaryWriter):
        raise NotImplementedError("This method is meant to be overridden!")

    def as_dict(self):
        raise NotImplementedError("This method is meant to be overridden!")

    def from_dict(self, d: dict):
        raise NotImplementedError("This method is meant to be overridden!")

    def __repr__(self):
        return f"<{self.__class__.__name__}>"
