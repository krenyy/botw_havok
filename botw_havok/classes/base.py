from ..binary import BinaryReader, BinaryWriter
from typing import List
from ..container.sections.hkobject import HKObject


if False:
    from ..hk import HK
    from ..container.sections.data import HKDataSection


class HKBase:
    hkClass: str
    hkobj: HKObject

    def __init__(self):
        self.hkobj = HKObject()

    def deserialize(self, hk: "HK", dsec: "HKDataSection", obj: HKObject):
        self.hkobj = obj
        self.hkClass = self.hkobj.hkclass.name

        self.hkobj.local_fixups.clear()

    def serialize(self, hk: "HK", dsec: "HKDataSection", bw: BinaryWriter):
        self.hkobj.data = bw.getvalue()
        self.hkobj.size = len(self.hkobj.data)

        dsec.objects.append(self.hkobj)

    def read_counter(self, hk: "HK", br: BinaryReader):
        hk._assert_pointer(br)
        count = br.read_int32()  # 0x0000000X
        br.read_uint32()  # 0x8000000X
        return count

    def write_counter(self, hk: "HK", bw: BinaryWriter, count: int):
        hk._write_empty_pointer(bw)
        bw.write_int32(count)
        bw.write_uint32(0x80000000 | count)

    def asdict(self):
        return {"hkClass": self.hkClass}
