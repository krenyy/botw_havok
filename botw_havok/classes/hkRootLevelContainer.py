from typing import List

from ..binary import BinaryReader, BinaryWriter
from ..binary.types import UInt32
from ..container.util.localfixup import LocalFixup
from ..container.util.localreference import LocalReference
from .base import HKBaseClass
from .common.hkRootLevelContainerNamedVariant import hkRootLevelContainerNamedVariant

if False:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkRootLevelContainer(HKBaseClass):
    namedVariants: List[hkRootLevelContainerNamedVariant]

    def __init__(self):
        super().__init__()

        self.namedVariants = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        ###

        namedVariantsCount_offset = br.tell()
        hkFile._assert_pointer(br)
        namedVariantsCount = hkFile._read_counter(br)

        for lfu in obj.local_fixups:
            br.step_in(lfu.dst)
            if lfu.src == namedVariantsCount_offset:
                for _ in range(namedVariantsCount):
                    nv = hkRootLevelContainerNamedVariant()
                    nv.deserialize(hkFile, br, obj)

                    self.namedVariants.append(nv)
            br.step_out()

        obj.local_fixups.clear()
        obj.global_references.clear()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().assign_class(hkFile, obj)

        ###

        namedVariantsCount_offset = bw.tell()
        hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.namedVariants)))

        bw.align_to(16)

        namedVariants_offset = bw.tell()
        for nV in self.namedVariants:
            nV.serialize(hkFile, bw, obj)

        ###

        super().serialize(hkFile, bw, obj)

    def asdict(self):
        d = super().asdict()
        d.update({"namedVariants": [nv.asdict() for nv in self.namedVariants]})
        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.namedVariants = [
            hkRootLevelContainerNamedVariant.fromdict(nv) for nv in d["namedVariants"]
        ]

        return inst

    def __repr__(self):
        return f"{self.__class__.__name__}({self.namedVariants})"
