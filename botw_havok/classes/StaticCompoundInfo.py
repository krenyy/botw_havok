from .base import HKBase
from typing import List
from .common.ActorInfo import ActorInfo
from .common.ShapeInfo import ShapeInfo
from ..binary import BinaryReader, BinaryWriter
from ..container.sections.util import LocalFixup

if False:
    from ..hk import HK
    from ..container.sections.data import HKDataSection
    from ..container.sections.hkobject import HKObject


class StaticCompoundInfo(HKBase):
    Offset: int
    ActorInfo: List[ActorInfo]
    ShapeInfo: List[ShapeInfo]

    def __init__(self):
        super().__init__()

        self.ActorInfo = []
        self.ShapeInfo = []

    def deserialize(self, hk: "HK", dsec: "HKDataSection", obj: "HKObject"):
        super().deserialize(hk, dsec, obj)

        br = BinaryReader(self.hkobj.data)
        br.big_endian = hk.header.endian == 0

        self.Offset = br.read_uint32()

        if not br.big_endian:
            br.read_uint32()

        ai_count = self.read_counter(hk, br)
        si_count = self.read_counter(hk, br)
        br.align_to(16)

        for _ in range(ai_count):
            ai = ActorInfo()
            ai.read(br)
            self.ActorInfo.append(ai)
        br.align_to(16)  # ?

        for _ in range(si_count):
            si = ShapeInfo()
            si.read(br)
            self.ShapeInfo.append(si)
        br.align_to(16)  # ?

    def serialize(self, hk: "HK", dsec: "HKDataSection"):
        bw = BinaryWriter()
        bw.big_endian = hk.header.endian == 0

        bw.write_uint32(self.Offset)

        if not bw.big_endian:
            bw.write_uint32(0)  # U64 instead of U32 for Switch?

        ai_count_offset = bw.tell()
        self.write_counter(hk, bw, len(self.ActorInfo))

        si_count_offset = bw.tell()
        self.write_counter(hk, bw, len(self.ShapeInfo))
        bw.align_to(16)

        ai_offset = bw.tell()
        [ai.write(bw) for ai in self.ActorInfo]
        bw.align_to(16)

        si_offset = bw.tell()
        [si.write(bw) for si in self.ShapeInfo]
        bw.align_to(16)

        self.hkobj.local_fixups.extend(
            [
                LocalFixup(ai_count_offset, ai_offset),
                LocalFixup(si_count_offset, si_offset),
            ]
        )

        super().serialize(hk, dsec, bw)

    def asdict(self):
        return (
            super()
            .asdict()
            .update(
                {
                    "ActorInfo": [ai.asdict() for ai in self.ActorInfo],
                    "ShapeInfo": [si.asdict() for si in self.ShapeInfo],
                }
            )
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.Offset}, {self.ActorInfo}, {self.ShapeInfo})"
