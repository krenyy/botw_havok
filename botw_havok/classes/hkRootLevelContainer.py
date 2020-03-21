from typing import List

from ..binary import BinaryReader, BinaryWriter
from ..container.sections.util import LocalFixup
from .base import HKBase
from .common.hkRootLevelContainerNamedVariant import hkRootLevelContainerNamedVariant

if False:
    from ..hk import HK
    from ..container.sections.hkobject import HKObject


class hkRootLevelContainer(HKBase):
    namedVariants: List[hkRootLevelContainerNamedVariant]

    def __init__(self):
        super().__init__()

        self.namedVariants = []

    def deserialize(self, hk: "HK", obj: "HKObject"):
        super().deserialize(hk, obj)

        br = BinaryReader(self.hkobj.bytes)
        br.big_endian = hk.header.endian == 0

        # namedVariantsCount_offset = br.tell()
        namedVariantsCount = hk._read_counter(br)
        br.align_to(16)  # TODO: Verify this

        # namedVariants_offset = br.tell()
        for _ in range(namedVariantsCount):
            nv = hkRootLevelContainerNamedVariant()
            self.namedVariants.append(nv)
            nv.deserialize(hk, br, self.hkobj)

        obj.local_fixups.clear()
        obj.global_references.clear()

    def serialize(self, hk: "HK"):
        super().assign_class(hk)

        bw = BinaryWriter()
        bw.big_endian = hk.header.endian == 0

        namedVariantsCounter_offset = bw.tell()
        hk._write_counter(bw, len(self.namedVariants))
        bw.align_to(16)

        namedVariants_offset = bw.tell()
        self.hkobj.local_fixups.append(
            LocalFixup(namedVariantsCounter_offset, namedVariants_offset)
        )

        for nv in self.namedVariants:
            nv.serialize(hk, self.hkobj, bw)

        super().serialize(hk, bw)

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
