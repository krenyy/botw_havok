from typing import List, Union

from ..binary import BinaryReader, BinaryWriter
from ..binary.types import UInt32, UInt64
from ..container.util.localfixup import LocalFixup
from ..container.util.localreference import LocalReference
from .base import HKBaseClass
from .common.ActorInfo import ActorInfo
from .common.ShapeInfo import ShapeInfo

if False:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class StaticCompoundInfo(HKBaseClass):
    Offset: Union[UInt32, UInt64]
    ActorInfo: List[ActorInfo]
    ShapeInfo: List[ShapeInfo]

    def __init__(self):
        super().__init__()

        self.ActorInfo = []
        self.ShapeInfo = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        ###

        if hkFile.header.pointer_size == 8:
            self.Offset = br.read_uint64()
        elif hkFile.header.pointer_size == 4:
            self.Offset = br.read_uint32()

        hkFile._assert_pointer(br)
        ai_count = hkFile._read_counter(br)

        hkFile._assert_pointer(br)
        si_count = hkFile._read_counter(br)

        br.align_to(16)

        for _ in range(ai_count):
            ai = ActorInfo()
            ai.deserialize(hkFile, br, obj)
            self.ActorInfo.append(ai)
        br.align_to(16)

        for _ in range(si_count):
            si = ShapeInfo()
            si.deserialize(hkFile, br, obj)
            self.ShapeInfo.append(si)
        br.align_to(16)

        obj.local_fixups.clear()
        obj.global_references.clear()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().assign_class(hkFile, obj)

        ###

        bw.reserve_uint32("EOF")

        if hkFile.header.padding_option:
            bw.write_uint32(UInt32(0))

        obj.local_references.extend(
            [
                LocalReference(hkFile, bw, obj, bw.tell(), self.ActorInfo),
                LocalReference(hkFile, bw, obj, bw.tell(), self.ShapeInfo),
            ]
        )

        bw.align_to(16)

        obj.reservations = bw.reservations

        ###

        super().serialize(hkFile, bw, obj)

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
