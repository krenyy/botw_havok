import typing
from io import BytesIO

from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32
from .localfixup import LocalFixup

if False:
    from ...hkfile import HKFile
    from ..sections.classnames.hkclass import HKClass
    from .localreference import LocalReference
    from .globalreference import GlobalReference


class HKObject:
    """Generic Havok data chunk
    """

    offset: UInt32
    hkClass: "HKClass"
    bytes: bytes = b""
    size: int

    local_fixups: typing.List[LocalFixup]

    local_references: typing.List["LocalReference"]
    global_references: typing.List["GlobalReference"]

    reservations: typing.Mapping[str, int]

    def __init__(self):
        self.local_fixups = []

        self.local_references = []
        self.global_references = []

        self.reservations = {}

    def resolve_local_fixups(self, hkFile: "HKFile"):
        hkFile.data.local_fixups.extend(
            [lfu + self.offset for lfu in self.local_fixups]
        )

    def resolve_local_references(self, bw: BinaryWriter):
        for lr in self.local_references:
            lr.resolve(bw, self)

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
