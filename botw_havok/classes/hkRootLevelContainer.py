from typing import List
from typing import TYPE_CHECKING

from .base import HKBaseClass
from .common.hkRootLevelContainerNamedVariant import hkRootLevelContainerNamedVariant
from ..binary import BinaryReader, BinaryWriter
from ..binary.types import Int32, UInt32
from ..container.util.globalreference import GlobalReference
from ..container.util.localfixup import LocalFixup

if TYPE_CHECKING:
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

        namedVariantsCount_offset = hkFile._assert_pointer(br)
        namedVariantsCount = hkFile._read_counter(br)

        for lfu in obj.local_fixups:
            br.step_in(lfu.dst)
            if lfu.src == namedVariantsCount_offset:
                for _ in range(namedVariantsCount):
                    nv = hkRootLevelContainerNamedVariant()
                    nv.deserialize(hkFile, br, obj)

                    self.namedVariants.append(nv)
            br.step_out()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().assign_class(hkFile, obj)

        ###

        namedVariantsCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.namedVariants)))

        bw.align_to(16)

        obj.local_fixups.append(LocalFixup(namedVariantsCount_offset, bw.tell()))

        [namedVariant.serialize(hkFile, bw, obj) for namedVariant in self.namedVariants]

        ####################
        # Write array data #
        ####################

        for namedVariant in self.namedVariants:
            obj.local_fixups.append(
                LocalFixup(namedVariant._namePointer_offset, bw.tell())
            )

            bw.write_string(namedVariant.name)
            bw.align_to(16)

            obj.local_fixups.append(
                LocalFixup(namedVariant._classNamePointer_offset, bw.tell())
            )

            bw.write_string(namedVariant.className)
            bw.align_to(16)

            gr = GlobalReference()
            gr.src_obj = obj
            gr.src_rel_offset = namedVariant._variantPointer_offset
            gr.dst_section_id = Int32(2)
            obj.global_references.append(gr)

            hkFile.data.objects.append(gr.dst_obj)

            namedVariant.variant.serialize(
                hkFile, BinaryWriter(big_endian=hkFile.header.endian == 0), gr.dst_obj
            )

        super().serialize(hkFile, bw, obj)

    def as_dict(self):
        d = super().as_dict()
        d.update({"namedVariants": [nv.as_dict() for nv in self.namedVariants]})
        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().from_dict(d).__dict__)

        inst.namedVariants = [
            hkRootLevelContainerNamedVariant.from_dict(nv) for nv in d["namedVariants"]
        ]

        return inst

    def __repr__(self):
        return f"{self.__class__.__name__}({self.namedVariants})"
