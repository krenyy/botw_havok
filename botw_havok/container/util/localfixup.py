from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32


class LocalFixup:
    src: UInt32
    dst: UInt32

    def __init__(self, src: UInt32 = None, dst: UInt32 = None):
        if src is not None and dst is not None:
            self.src = src
            self.dst = dst

    def read(self, br: BinaryReader):
        self.src = br.read_uint32()
        self.dst = br.read_uint32()

    def write(self, bw: BinaryWriter):
        bw.write_uint32(self.src)
        bw.write_uint32(self.dst)

    def __add__(self, value: UInt32):
        return LocalFixup(self.src + value, self.dst + value)

    def __sub__(self, value: UInt32):
        return LocalFixup(self.src - value, self.dst - value)

    def __eq__(self, value: object):
        if not isinstance(value, LocalFixup):
            raise NotImplementedError()
        return (self.src == value.src) and (self.dst == value.dst)

    def __gt__(self, value: object):
        if not isinstance(value, LocalFixup):
            raise NotImplementedError()
        return self.src > value.src

    def __hash__(self):
        return hash((self.src, self.dst))

    def __repr__(self):
        return f"{self.__class__.__name__}({hex(self.src)}, {hex(self.dst)})"
