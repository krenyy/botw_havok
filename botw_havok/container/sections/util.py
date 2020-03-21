from typing import Union

from ...binary import BinaryReader, BinaryWriter

if False:
    from .data import HKObject


class LocalFixup:
    src: int
    dst: int

    def __init__(self, src: int = None, dst: int = None):
        if src is not None and dst is not None:
            self.src = src
            self.dst = dst

    def read(self, br: BinaryReader):
        self.src = br.read_uint32()
        self.dst = br.read_uint32()

    def write(self, bw: BinaryWriter):
        bw.write_uint32(self.src)
        bw.write_uint32(self.dst)

    def __add__(self, value: Union[int, "LocalFixup"]):
        lfu = LocalFixup()
        if isinstance(value, int):
            lfu.src = self.src + value
            lfu.dst = self.dst + value
        elif isinstance(value, "LocalFixup"):
            lfu.src = self.src + value.src
            lfu.dst = self.dst + value.dst
        else:
            raise NotImplementedError("Invalid addition type!")
        return lfu

    def __sub__(self, value: Union[int, "LocalFixup"]):
        lfu = LocalFixup()
        if isinstance(value, int):
            lfu.src = self.src - value
            lfu.dst = self.dst - value
        elif isinstance(value, "LocalFixup"):
            lfu.src = self.src - value.src
            lfu.dst = self.dst - value.dst
        else:
            raise NotImplementedError("Invalid subtraction type!")
        return lfu

    def __eq__(self, value: "LocalFixup"):
        return (self.src == value.src) and (self.dst == value.dst)

    def __hash__(self):
        return hash((self.src, self.dst))

    def __repr__(self):
        return f"{self.__class__.__name__}({hex(self.src)}, {hex(self.dst)})"


class GlobalFixup:
    src: int
    dst_section_id: int
    dst: int

    def read(self, br: BinaryReader):
        self.src = br.read_uint32()
        self.dst_section_id = br.read_int32()
        self.dst = br.read_uint32()

    def write(self, bw: BinaryWriter):
        bw.write_uint32(self.src)
        bw.write_int32(self.dst_section_id)
        bw.write_uint32(self.dst)

    def __eq__(self, value: "GlobalFixup"):
        return (
            (self.src == value.src)
            and (self.dst_section_id == value.dst_section_id)
            and (self.dst == value.dst)
        )

    def __hash__(self):
        return hash((self.src, self.dst_section_id, self.dst))

    def __repr__(self):
        return f"{self.__class__.__name__}({hex(self.src)}, {hex(self.dst)})"


class GlobalReference:
    src_obj: "HKObject"
    dst_obj: "HKObject"

    dst_section_id: int = 2  # __data__

    src_rel_offset: int
    dst_rel_offset: int = 0  # Should always point to the beginning

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.src_obj.hkclass.name}@{hex(self.src_rel_offset)}, "
            f"{self.dst_obj.hkclass.name}@{hex(self.dst_rel_offset)})"
        )

    def __hash__(self):
        return hash(
            (self.src_obj, self.dst_obj, self.src_rel_offset, self.dst_rel_offset)
        )
