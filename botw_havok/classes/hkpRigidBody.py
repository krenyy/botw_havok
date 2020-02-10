from ..binary import BinaryReader, BinaryWriter
from ..container.sections.util import HKChunkLink, HKDataLink
from .base import HKChunk

if False:
    from ..hk import Havok
    from ..container.sections import HKDataSection


class HKPRigidBody(HKChunk):
    """hkpRigidBody, contains shapes (hkpBvCompressedMeshShape, hkpBoxShape)

       Most of the data here is unknown
    """

    name: str

    def read(self, hk: "Havok", br: BinaryReader):
        if hk.header.pointer_size == 8:
            br.seek_relative(+0x2D0)
        elif hk.header.pointer_size == 4:
            br.seek_relative(+0x220)
        else:
            raise NotImplementedError("Invalid pointer size")

        self.name = br.read_string()
        br.align_to(16)

    def write(self, hk: "Havok", sec: "HKDataSection", bw: BinaryWriter):
        if sec.links:
            sec.links[-1].dst = bw.tell() - sec.abs_offset

        self.write_pointer(hk, bw)
        self.write_pointer(hk, bw)
        self.write_pointer(hk, bw)
        self.write_pointer(hk, bw)

        # Chunk link base, points to children
        link = HKChunkLink()
        link.src = bw.tell() - sec.abs_offset
        link.dst_section_id = 2
        sec.links.append(link)

        self.write_pointer(hk, bw)

        bw.write_uint32(0xFFFFFFFF)

        # -------------------------

        self.write_pointer(hk, bw)
        self.write_pointer(hk, bw)
        bw.align_to(16)

        bw.write_int8(0)
        bw.write_int8(8)  # ?
        bw.write_int8(0)
        bw.write_int8(0)

        bw.write_int32(0)

        bw.write_int8(1)
        bw.write_int8(0)
        bw.write_int8(0)
        bw.write_int8(0)

        bw.write_uint32(0x90000000)

        bw.write_int64(0)
        bw.write_int64(0)
        bw.write_int64(0)
        bw.write_int64(0)

        self.write_pointer(hk, bw)
        self.write_pointer(hk, bw)
        self.write_pointer(hk, bw)

        bw.write_uint32(0x7F7FFFEE)
        bw.align_to(16)

        self.write_counter(hk, bw, 0)  # ?
        bw.align_to(16)

        self.write_pointer(hk, bw)
        self.write_pointer(hk, bw)

        # Link source
        pointer = HKDataLink()
        pointer.src = bw.tell() - sec.abs_offset

        self.write_pointer(hk, bw)
        self.write_pointer(hk, bw)

        bw.write_int32(0)
        bw.write_uint32(0x80000000)

        bw.write_int8(1)
        bw.write_int8(0)
        bw.write_int8(0)
        bw.write_int8(0)

        bw.write_uint32(0x3F000000)

        bw.write_single(0.5)
        bw.write_single(0.4)

        bw.write_int32(0)
        if hk.header.padding_option == 1:
            bw.write_int64(0)

        bw.write_single(1.0)

        self.write_pointer(hk, bw)
        self.write_pointer(hk, bw)

        bw.write_uint32(0xFFFFFFFF)

        # -------------------------

        self.write_pointer(hk, bw)
        self.write_pointer(hk, bw)

        self.write_counter(hk, bw, 0)  # ?
        self.write_counter(hk, bw, 0)  # ?

        self.write_pointer(hk, bw)

        bw.write_int8(0)
        bw.write_int8(1)
        bw.write_int8(0)
        bw.write_int8(0)

        bw.write_uint32(0xFFFFFFFF)

        # -------------------------

        self.write_pointer(hk, bw)

        bw.write_int8(0)
        bw.write_int8(0)
        bw.write_int8(3)
        bw.write_int8(1)

        self.write_pointer(hk, bw)
        self.write_pointer(hk, bw)
        self.write_pointer(hk, bw)

        bw.write_int8(5)
        bw.write_int8(15)

        bw.write_int16(0xC000)  # half-float: -2.0
        bw.write_int16(0xC000)

        bw.write_int8(0)  # Padding?
        bw.write_int8(0)
        bw.align_to(16)

        # fmt:off
        bw.write_matrix4x4([
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        ])

        bw.write_matrix4x4([
            0.0, 0.0, 0.0, 0.000000,
            0.0, 0.0, 0.0, 0.000000,
            0.0, 0.0, 0.0, 0.999999,
            0.0, 0.0, 0.0, 0.999999,
        ])
        # fmt:on

        # Skip 32 bytes
        bw.write_int64(0)
        bw.write_int64(0)
        bw.write_int64(0)
        bw.write_int64(0)

        bw.write_uint32(0x400FE872)

        bw.write_int8(0)
        bw.write_int8(0)
        bw.write_int16(0x3D4D)

        bw.write_uint16(0x3F80)
        bw.write_int8(0x7F)

        bw.write_int8(1)
        bw.write_int8(0)
        bw.write_int8(0)
        bw.write_int8(0)

        # Skip 83/96 bytes
        bw.write_int64(0)
        bw.write_int64(0)
        bw.write_int64(0)
        bw.write_int64(0)

        bw.write_int64(0)
        bw.write_int64(0)
        bw.write_int64(0)
        bw.write_int64(0)

        bw.write_int64(0)
        bw.write_int64(0)

        if hk.header.pointer_size == 8:
            bw.write_int64(0)
            bw.write_int64(0)
        elif hk.header.pointer_size == 4:
            bw.write_int32(0)
            bw.write_int32(0)
            bw.write_int32(0)

        bw.write_single(1.0)

        self.read_pointer(hk, bw)
        self.read_pointer(hk, bw)
        self.read_pointer(hk, bw)
        self.read_pointer(hk, bw)
        self.read_pointer(hk, bw)
        self.read_pointer(hk, bw)

        bw.write_uint32(0xFFFFFFFF)
        bw.align_to(16)

        # Link destination always before RigidBody name
        pointer.dst = bw.tell() - sec.abs_offset
        sec.pointers.append(pointer)

        bw.write_string(self.name)
        bw.align_to(16)
