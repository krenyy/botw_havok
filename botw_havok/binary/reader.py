__all__ = ("BinaryReader",)


import struct

import numpy as np

from ..util import Matrix, Vector3, Vector4
from .base import BinaryBase


class BinaryReader(BinaryBase):
    # READ

    def __init__(self, initial_bytes=None):
        super().__init__(initial_bytes=initial_bytes)

    def read_type(self, struct_type: str, value: bytes):
        return struct.unpack(
            f"{self.endian_char()}{self.type_names[struct_type]}", value
        )[0]

    def read_int8(self) -> int:
        return self.read_type(struct_type="int8", value=self.read(1))

    def read_uint8(self) -> int:
        return self.read_type(struct_type="uint8", value=self.read(1))

    def read_int16(self) -> int:
        return self.read_type(struct_type="int16", value=self.read(2))

    def read_uint16(self) -> int:
        return self.read_type(struct_type="uint16", value=self.read(2))

    def read_int32(self) -> int:
        return self.read_type(struct_type="int32", value=self.read(4))

    def read_uint32(self) -> int:
        return self.read_type(struct_type="uint32", value=self.read(4))

    def read_int64(self) -> int:
        return self.read_type(struct_type="int64", value=self.read(8))

    def read_uint64(self) -> int:
        return self.read_type(struct_type="uint64", value=self.read(8))

    def read_floatu8(self) -> float:
        return (self.read_uint8() * 1) / 0xFF

    def read_half(self) -> float:
        return float(np.frombuffer(self.read(2), dtype=f"{self.endian_char()}f2")[0])

    def read_single(self) -> float:
        return self.read_type(struct_type="float", value=self.read(4))

    def read_double(self) -> float:
        return self.read_type(struct_type="double", value=self.read(8))

    def read_vector3(self) -> Vector3:
        x: float = self.read_single()
        y: float = self.read_single()
        z: float = self.read_single()
        return Vector3(x, y, z)

    def read_vector4(self) -> Vector4:
        return Vector4(v3=self.read_vector3(), w=self.read_single())

    def read_matrix(self, size: int) -> Matrix:
        return Matrix([self.read_vector4() for _ in range(size)])

    def read_string(self, size: int = None, encoding: str = "utf-8") -> str:
        if not size:
            ret = self._read_terminated_string()
        else:
            ret = struct.unpack(f"{self.endian_char()}{f'{size}s'}", self.read(size))
            ret = ret[0].rstrip(b"\x00")

        return ret.decode(encoding)

    def _read_terminated_string(self) -> bytes:
        ret = []
        c = b""
        while c != b"\x00":
            ret.append(c)
            c = self.read(1)
            if not c:
                raise ValueError(f"Unterminated string: {ret}")
        return b"".join(ret)

    # ASSERTS

    def assert_int8(self, *args: int) -> int:
        ret = self.read_int8()
        assert ret in args
        return ret

    def assert_uint8(self, *args: int) -> int:
        ret = self.read_uint8()
        assert ret in args
        return ret

    def assert_int16(self, *args: int) -> int:
        ret = self.read_int16()
        assert ret in args
        return ret

    def assert_uint16(self, *args: int) -> int:
        ret = self.read_uint16()
        assert ret in args
        return ret

    def assert_int32(self, *args: int) -> int:
        ret = self.read_int32()
        assert ret in args
        return ret

    def assert_uint32(self, *args: int) -> int:
        ret = self.read_uint32()
        assert ret in args
        return ret

    def assert_int64(self, *args: int) -> int:
        ret = self.read_int64()
        assert ret in args
        return ret

    def assert_uint64(self, *args: int) -> int:
        ret = self.read_uint64()
        assert ret in args
        return ret

    def assert_single(self, *args: float) -> float:
        ret = self.read_single()
        assert ret in args
        return ret

    def assert_double(self, *args: float) -> float:
        ret = self.read_double()
        assert ret in args
        return ret

    def assert_string(self, *args: str, size: int) -> str:
        ret = self.read_string(size)
        assert ret in args
        return ret

    # NAVIGATION

    def align_to(self, alignment: int):
        if alignment <= 0:
            raise Exception("Not possible")
        dist = alignment - (self.tell() % alignment)
        if not dist == alignment:
            return self.seek_relative(dist)

    def peek(self):
        ret = self.read(1)
        self.seek_relative(-1)
        return ret

    def skip(self, char: bytes = b"\xFF"):
        skipped_bytes = 0
        while self.read(1) in char:
            skipped_bytes += 1
        self.seek_relative(-1)
        return skipped_bytes
