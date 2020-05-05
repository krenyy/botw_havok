__all__ = ("BinaryReader",)


import struct

import numpy as np

from .base import BinaryBase
from .types import (
    Int8,
    Int16,
    Int32,
    Int64,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
    Float16,
    Float32,
    Float64,
    String,
    Vector3,
    Vector4,
    Matrix,
)


class BinaryReader(BinaryBase):
    # READ

    def __init__(self, initial_bytes=None, big_endian: bool = None):
        super().__init__(initial_bytes=initial_bytes, big_endian=big_endian)

    def read_type(self, struct_type: str, value: bytes):
        return struct.unpack(
            f"{self.endian_char()}{self.struct_types[struct_type]}", value
        )[0]

    def read_int8(self) -> Int8:
        return Int8(self.read_type(struct_type="i8", value=self.read(1)))

    def read_uint8(self) -> UInt8:
        return UInt8(self.read_type(struct_type="u8", value=self.read(1)))

    def read_int16(self) -> Int16:
        return Int16(self.read_type(struct_type="i16", value=self.read(2)))

    def read_uint16(self) -> UInt16:
        return UInt16(self.read_type(struct_type="u16", value=self.read(2)))

    def read_int32(self) -> Int32:
        return Int32(self.read_type(struct_type="i32", value=self.read(4)))

    def read_uint32(self) -> UInt32:
        return UInt32(self.read_type(struct_type="u32", value=self.read(4)))

    def read_int64(self) -> Int64:
        return Int64(self.read_type(struct_type="i64", value=self.read(8)))

    def read_uint64(self) -> UInt64:
        return UInt64(self.read_type(struct_type="u64", value=self.read(8)))

    def read_float16(self) -> Float16:
        return Float16(np.frombuffer(self.read(2), dtype=f"{self.endian_char()}f2")[0])

    def read_float32(self) -> Float32:
        return Float32(self.read_type(struct_type="f32", value=self.read(4)))

    def read_float64(self) -> Float64:
        return Float64(self.read_type(struct_type="f64", value=self.read(8)))

    def read_vector3(self) -> Vector3:
        return Vector3(*[self.read_float32() for _ in range(3)])

    def read_vector4(self) -> Vector4:
        return Vector4(*[self.read_float32() for _ in range(4)])

    def read_matrix(self, size: int) -> Matrix:
        return Matrix(*[self.read_vector4() for _ in range(size)])

    def read_string(self, size: int = None, encoding: str = "utf-8") -> String:
        if not size:
            ret = self._read_terminated_string()
        else:
            ret = struct.unpack(f"{self.endian_char()}{f'{size}s'}", self.read(size))[0]
            ret = ret.rstrip(b"\x00")

        return String(ret.decode(encoding))

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

    def assert_int8(self, *args: Int8) -> Int8:
        ret = self.read_int8()
        assert ret in args
        return ret

    def assert_uint8(self, *args: UInt8) -> UInt8:
        ret = self.read_uint8()
        assert ret in args
        return ret

    def assert_int16(self, *args: Int16) -> Int16:
        ret = self.read_int16()
        assert ret in args
        return ret

    def assert_uint16(self, *args: UInt16) -> UInt16:
        ret = self.read_uint16()
        assert ret in args
        return ret

    def assert_int32(self, *args: Int32) -> Int32:
        ret = self.read_int32()
        assert ret in args
        return ret

    def assert_uint32(self, *args: UInt32) -> UInt32:
        ret = self.read_uint32()
        assert ret in args
        return ret

    def assert_int64(self, *args: Int64) -> Int64:
        ret = self.read_int64()
        assert ret in args
        return ret

    def assert_uint64(self, *args: UInt64) -> UInt64:
        ret = self.read_uint64()
        assert ret in args
        return ret

    def assert_float16(self, *args: Float16) -> Float16:
        ret = self.read_float16()
        assert ret in args
        return ret

    def assert_float32(self, *args: Float32) -> Float32:
        ret = self.read_float32()
        assert ret in args
        return ret

    def assert_float64(self, *args: Float64) -> Float64:
        ret = self.read_float64()
        assert ret in args
        return ret

    def assert_string(self, *args: String, size: int) -> String:
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

    def peek(self, distance: int = 1):
        ret = self.read(distance)
        self.seek_relative(-distance)
        return ret
