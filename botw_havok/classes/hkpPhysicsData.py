from ..binary import BinaryReader, BinaryWriter
from ..container.sections.util import GlobalFixup, GlobalReference, LocalFixup
from .base import HKBase

if False:
    from ..hk import HK
    from ..container.sections.data import HKDataSection, HKObject


class HKPPhysicsData(HKBase):
    """Physics data container
    """

    unknownCount: int  # TODO: figure out what this is

    def deserialize(self, hk: "HK", dsec: "HKDataSection", obj: "HKObject"):
        self.hkobj = obj

        br = BinaryReader(self.hkobj.data)
        br.big_endian = hk.header.endian == 0

        hk._assert_pointer(br)
        hk._assert_pointer(br)
        hk._assert_pointer(br)

        self.unknownCount = self.read_counter(hk, br)
        br.align_to(16)

        physicsSystemCount = len(
            [o for o in dsec.objects if o.hkclass.name == "hkpPhysicsSystem"]
        )

        for _ in range(physicsSystemCount):
            hk._assert_pointer(br)

    def serialize(self, hk: "HK", dsec: "HKDataSection"):
        bw = BinaryWriter()
        bw.big_endian = hk.header.endian == 0

        hk._write_empty_pointer(bw)
        hk._write_empty_pointer(bw)
        hk._write_empty_pointer(bw)

        lfu = LocalFixup()
        lfu.src = bw.tell() - dsec.absolute_offset
        self.write_counter(hk, bw, self.unknownCount)  # ?
        bw.align_to(16)
        lfu.dst = bw.tell() - dsec.absolute_offset
        hk.pointers.append(pointer)

        link = HKChunkLink()
        link.src = bw.tell() - sec.abs_offset
        link.dst_section_id = 2
        sec.links.append(link)

        bw.write_int64(0)
        bw.write_int64(0)
