from typing import List

from ..binary import BinaryReader, BinaryWriter
from ..container.sections.util import LocalFixup
from .base import HKBase
from .common.ActorInfo import ActorInfo
from .common.ShapeInfo import ShapeInfo

if False:
    from ..hk import HK
    from ..container.sections.hkobject import HKObject


class StaticCompoundInfo(HKBase):
    Offset: int
    ActorInfo: List[ActorInfo]
    ShapeInfo: List[ShapeInfo]

    def __init__(self):
        super().__init__()

        self.ActorInfo = []
        self.ShapeInfo = []

    def deserialize(self, hk: "HK", obj: "HKObject"):
        super().deserialize(hk, obj)

        br = BinaryReader(obj.bytes)
        br.big_endian = hk.header.endian == 0

        self.Offset = br.read_uint32()

        if not br.big_endian:
            br.seek_relative(+4)

        ai_count = hk._read_counter(br)
        si_count = hk._read_counter(br)
        br.align_to(16)

        for _ in range(ai_count):
            ai = ActorInfo()
            ai.read(br)
            self.ActorInfo.append(ai)
        br.align_to(16)

        for _ in range(si_count):
            si = ShapeInfo()
            si.read(br)
            self.ShapeInfo.append(si)
        br.align_to(16)

        obj.local_fixups.clear()
        obj.global_references.clear()

    def serialize(self, hk: "HK"):
        super().assign_class(hk)

        bw = BinaryWriter()
        bw.big_endian = hk.header.endian == 0

        bw.reserve_uint32("EOF")

        if hk.header.padding_option:  # probably
            bw.write_uint32(0)

        ai_count_offset = bw.tell()
        hk._write_counter(bw, len(self.ActorInfo))

        si_count_offset = bw.tell()
        hk._write_counter(bw, len(self.ShapeInfo))
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

        self.hkobj.reservations = bw.reservations

        super().serialize(hk, bw)

    def asdict(self):
        d = super().asdict()
        d.update(
            {
                "ActorInfo": [ai.asdict() for ai in self.ActorInfo],
                "ShapeInfo": [si.asdict() for si in self.ShapeInfo],
            }
        )
        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.hkClass = d["hkClass"]
        inst.ActorInfo = [ActorInfo.fromdict(ai) for ai in d["ActorInfo"]]
        inst.ShapeInfo = [ShapeInfo.fromdict(si) for si in d["ShapeInfo"]]

        return inst

    def __repr__(self):
        return f"{self.__class__.__name__}({self.ActorInfo}, {self.ShapeInfo})"
