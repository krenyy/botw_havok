import typing

from ...binary import BinaryReader, BinaryWriter
from .util import GlobalReference, LocalFixup

if False:
    from ...hk import HK
    from .classnames import HKClass
    from .data import HKDataSection


class HKObject:
    """Generic Havok data chunk
    """

    offset: int
    hkclass: "HKClass"
    bytes: bytes = b""
    size: int

    local_fixups: typing.List[LocalFixup]
    global_references: typing.List[GlobalReference]

    reservations: typing.Mapping[str, int]

    def __init__(self):
        self.local_fixups = []
        self.global_references = []
        self.reservations = {}

    def resolve_local_fixups(self, hk: "HK"):
        hk.data.local_fixups.extend([lfu + self.offset for lfu in self.local_fixups])

    def resolve_global_references(self, hk: "HK"):
        for gr in self.global_references:
            if gr not in hk.data.global_references:
                hk.data.global_references.append(gr)

    def read(self, hk: "HK", br: BinaryReader, size: int):
        self.offset = br.tell() - hk.data.absolute_offset
        self.bytes = br.read(size)

    def write(self, hk: "HK", bw: BinaryWriter):
        self.offset = bw.tell() - hk.data.absolute_offset
        bw.write(self.bytes)

        self.resolve_local_fixups(hk)
        self.resolve_global_references(hk)

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.hkclass.name})>"
