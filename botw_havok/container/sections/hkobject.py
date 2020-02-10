import typing

from ...binary import BinaryReader, BinaryWriter
from .classnames import HKClass
from .util import GlobalReference, LocalFixup

if False:
    from ...hk import HK
    from .data import HKDataSection


class HKObject:
    """Generic Havok data chunk
    """

    offset: int
    hkclass: HKClass
    data: bytes
    size: int

    local_fixups: typing.List[LocalFixup]
    global_references: typing.List[GlobalReference]

    reservations: typing.Mapping[str, int]

    def __init__(self):
        self.local_fixups = []
        self.global_references = []
        self.reservations = {}

    def set_curr_offset(
        self, dsec: "HKDataSection", brw: typing.Union[BinaryReader, BinaryWriter]
    ):
        self.offset = brw.tell() - dsec.absolute_offset

    def resolve_local_fixups(self, dsec: "HKDataSection"):
        dsec.local_fixups.extend([lfu + self.offset for lfu in self.local_fixups])

    def resolve_global_references(self, dsec: "HKDataSection"):
        for gr in self.global_references:
            if gr not in dsec.global_references:
                dsec.global_references.append(gr)

    def read(self, hk: "HK", dsec: "HKDataSection", br: BinaryReader, size: int):
        self.set_curr_offset(dsec, br)
        self.data = br.read(size)

    def write(self, hk: "HK", dsec: "HKDataSection", bw: BinaryWriter):
        self.set_curr_offset(dsec, bw)
        bw.write(self.data)

        self.resolve_local_fixups(dsec)
        self.resolve_global_references(dsec)

    def asdict(self):
        raise NotImplementedError(
            "It's not possible to convert a serialized object to dict!"
        )

    @classmethod
    def fromdict(self, d: dict):
        raise NotImplementedError()

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.hkclass.name})>"
