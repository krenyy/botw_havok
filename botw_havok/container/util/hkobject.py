from io import BytesIO
from typing import Dict, List
from typing import TYPE_CHECKING

from .localfixup import LocalFixup
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ..sections.classnames.hkclass import HKClass
    from .globalreference import GlobalReference


class HKObject:
    """Generic Havok data chunk
    """

    offset: UInt32
    hkClass: "HKClass"
    bytes: bytes = b""
    size: int

    local_fixups: List[LocalFixup]
    global_references: List["GlobalReference"]

    reservations: Dict[str, UInt32]

    def __init__(self):
        self.local_fixups = []
        self.global_references = []

        self.reservations = {}

    def resolve_local_fixups(self, hkFile: "HKFile"):
        hkFile.data.local_fixups.extend(
            [lfu + self.offset for lfu in self.local_fixups]
        )

    def resolve_global_references(self, hkFile: "HKFile"):
        for gr in self.global_references:
            if gr not in hkFile.data.global_references:
                hkFile.data.global_references.append(gr)

    def read(self, hkFile: "HKFile", br: BinaryReader, size: int):
        self.offset = br.tell() - hkFile.data.absolute_offset
        self.bytes = br.read(size)

    def write(self, hkFile: "HKFile", bw: BinaryWriter):
        self.offset = bw.tell() - hkFile.data.absolute_offset
        BytesIO.write(bw, self.bytes)

        self.resolve_local_fixups(hkFile)
        self.resolve_global_references(hkFile)

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.hkClass.name})>"
