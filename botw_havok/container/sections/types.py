from ...binary import BinaryReader, BinaryWriter
from .base import HKSection


class HKTypesSection(HKSection):
    """Havok __types__ section, seems unused
    """

    id: int = 1
    tag: str = "__types__"

    def read(self, br: BinaryReader):
        super().read(br)

    def write(self, bw: BinaryWriter):
        self.absolute_offset = bw.tell()
        self.localfixups_offset = bw.tell() - self.absolute_offset
        self.globalfixups_offset = bw.tell() - self.absolute_offset
        self.virtualfixups_offset = bw.tell() - self.absolute_offset
        self.exports_offset = bw.tell() - self.absolute_offset
        self.imports_offset = bw.tell() - self.absolute_offset
        self.EOF_offset = bw.tell() - self.absolute_offset

        bw.fill_uint32(f"{self.tag}abs", self.absolute_offset)
        bw.fill_uint32(f"{self.tag}loc", self.localfixups_offset)
        bw.fill_uint32(f"{self.tag}glob", self.globalfixups_offset)
        bw.fill_uint32(f"{self.tag}virt", self.virtualfixups_offset)
        bw.fill_uint32(f"{self.tag}exp", self.exports_offset)
        bw.fill_uint32(f"{self.tag}imp", self.imports_offset)
        bw.fill_uint32(f"{self.tag}eof", self.EOF_offset)

    def __repr__(self):
        return f"<{self.__class__.__name__} ()>"
