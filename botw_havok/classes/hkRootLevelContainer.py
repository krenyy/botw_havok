# pylama:ignore=E501
from ..binary import BinaryReader, BinaryWriter
from ..container.sections.util import GlobalFixup, GlobalReference, LocalFixup
from .base import HKBase
import typing

if False:
    from ..hk import HK
    from ..container.sections import HKDataSection, HKObject


class HKRootLevelContainer(HKBase):
    """Root class of every BotW Havok file
    """

    physicsDataCount: int  # ?
    childName: str
    childClass: str

    def __init__(self, d: dict = None):
        if d:
            (
                self.hkClass,
                self.physicsDataCount,
                self.childName,
                self.childClass,
            ) = d.values()

    def deserialize(self, hk: "HK", dsec: "HKDataSection", obj: "HKObject"):
        super().deserialize(hk, dsec, obj)

        br = BinaryReader(self.hkobj.data)
        br.big_endian = hk.header.endian == 0

        self.physicsDataCount = self.read_counter(hk, br)
        br.align_to(16)

        hk._assert_pointer(br)
        hk._assert_pointer(br)
        hk._assert_pointer(br)

        self.childName = br.read_string()
        br.align_to(16)

        self.childClass = br.read_string()
        br.align_to(16)

    def serialize(self, hk: "HK", dsec: "HKDataSection"):
        bw = BinaryWriter()
        bw.big_endian = hk.header.endian == 0

        local_fixups: typing.List[LocalFixup] = []

        lfu = LocalFixup()
        lfu.src = bw.tell() - self.hkobj.offset
        self.write_counter(hk, bw, self.physics_data_count)  # Should always be 1
        bw.align_to(16)
        lfu.dst = bw.tell() - self.hkobj.offset
        local_fixups.append(lfu)

        lfu = LocalFixup()
        lfu.src = bw.tell() - self.hkobj.offset
        hk._write_empty_pointer(bw)
        hk._write_empty_pointer(bw)

        gfu = GlobalFixup()
        gfu.src = bw.tell() - self.hkobj.offset
        gfu.dst_section_id = dsec.id
        dsec.global_fixups.append(gfu)
        hk._write_empty_pointer(bw)

        lfu.dst = bw.tell() - self.hkobj.offset
        local_fixups.append(lfu)

        lfu = LocalFixup()
        lfu.src = bw.tell() - self.hkobj.offset - (2 * hk.header.pointer_size)
        bw.write_string(self.physics_data_name)
        bw.align_to(16)
        lfu.dst = bw.tell() - self.hkobj.offset
        local_fixups.append(lfu)

        bw.write_string(self.physics_data_class)
        bw.align_to(16)

        self.hkobj.data = bw.getvalue()
        self.hkobj.local_fixups = local_fixups

    def asdict(self):
        return {
            "physicsDataCount": self.physicsDataCount,
            "childName": self.childName,
            "childClass": self.childClass,
        }

    @classmethod
    def fromdict(cls, d: dict):
        return cls(d)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.physicsDataCount}, {self.childName}, {self.childClass})"
