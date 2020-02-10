from ..binary import BinaryReader, BinaryWriter
from ..container.sections.util import HKChunkLink, HKDataLink
from .base import HKChunk

if False:
    from ..hk import Havok
    from ..container.sections import HKDataSection


class HKPPhysicsSystem(HKChunk):
    """Physics system, usually contains a hkpRigidBody
    """

    linked_chunks_count: int
    name: str

    def read(self, hk: "Havok", br: BinaryReader):
        self.read_pointer(hk, br)
        self.read_pointer(hk, br)

        self.children_count = self.read_counter(hk, br)
        self.read_counter(hk, br)
        self.read_counter(hk, br)
        self.read_counter(hk, br)

        br.assert_int8(1)  # Unknown, always 1
        br.align_to(16)

        br.seek_relative(+16)  # Padding?

        self.name = br.read_string()  # 'Default Physics System'
        br.align_to(16)

    def write(self, hk: "Havok", sec: "HKDataSection", bw: BinaryWriter):
        if sec.links:
            sec.links[-1].dst = bw.tell() - sec.abs_offset

        self.write_pointer(hk, bw)
        self.write_pointer(hk, bw)

        pointer = HKDataLink()
        pointer.src = bw.tell() - sec.abs_offset

        self.write_counter(hk, bw, self.children_count)
        self.write_counter(hk, bw, 0)
        self.write_counter(hk, bw, 0)
        self.write_counter(hk, bw, 0)

        self.write_pointer(hk, bw)
        self.write_pointer(hk, bw)

        bw.write_int8(1)  # ?
        bw.write_int8(0)
        bw.write_int8(0)
        bw.write_int8(0)
        bw.align_to(16)

        pointer.dst = bw.tell() - sec.abs_offset
        sec.pointers.append(pointer)

        link = HKChunkLink()
        link.src = bw.tell() - sec.abs_offset
        link.dst_section_id = 2

        pointer = HKDataLink()
        pointer.src = bw.tell() - sec.abs_offset - 0x10 - (2 * hk.header.pointer_size)
        bw.seek_relative(+16)  # Padding?
        pointer.dst = bw.tell() - sec.abs_offset

        bw.write_string(self.name)
        bw.align_to(16)
