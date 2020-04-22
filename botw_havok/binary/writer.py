__all__ = ("BinaryWriter",)


import struct
import typing

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


class BinaryWriter(BinaryBase):
    reservations: typing.Dict[str, int]

    def __init__(self, initial_bytes=None, big_endian: bool = None):
        super().__init__(initial_bytes=initial_bytes, big_endian=big_endian)

        self.reservations = {}

        self.types = {
            Int8: self.write_int8,
            Int16: self.write_int16,
            Int32: self.write_int32,
            Int64: self.write_int64,
            UInt8: self.write_uint8,
            UInt16: self.write_uint16,
            UInt32: self.write_uint32,
            UInt64: self.write_uint64,
            Float16: self.write_float16,
            Float32: self.write_float32,
            Float64: self.write_float64,
            String: self.write_string,
            Vector3: self.write_vector3,
            Vector4: self.write_vector4,
            Matrix: self.write_matrix,
        }

    # WRITE

    def write(self, value):
        """Writes value as bytes depending on it's type
        """
        if isinstance(value, list):
            [self.write(i) for i in value]
        else:
            try:
                return self.types[type(value)](value)
            except KeyError:
                raise NotImplementedError("Invalid variable type!")

    def write_type(self, type: str, value):
        return super().write(
            struct.pack(f"{self.endian_char()}{self.struct_types[type]}", value)
        )

    def write_int8(self, num: Int8):
        return self.write_type("i8", num)

    def write_uint8(self, num: UInt8):
        return self.write_type("u8", num)

    def write_int16(self, num: Int16):
        return self.write_type("i16", num)

    def write_uint16(self, num: UInt16):
        return self.write_type("u16", num)

    def write_int32(self, num: Int32):
        return self.write_type("i32", num)

    def write_uint32(self, num: UInt32):
        return self.write_type("u32", num)

    def write_int64(self, num: Int64):
        return self.write_type("i64", num)

    def write_uint64(self, num: UInt64):
        return self.write_type("u64", num)

    def write_float16(self, num: Float16):
        return super().write(np.array([num], dtype=f"{self.endian_char()}f2").tobytes())

    def write_float32(self, num: Float32):
        return self.write_type("f32", num)

    def write_float64(self, num: Float64):
        return self.write_type("f64", num)

    def write_vector3(self, vector: Vector3):
        return super().write(struct.pack(f"{self.endian_char()}3f", *vector))

    def write_vector4(self, vector: Vector4):
        return super().write(struct.pack(f"{self.endian_char()}4f", *vector))

    def write_matrix(self, matrix: Matrix):
        return [self.write_vector4(v) for v in matrix]

    def write_string(self, string: String, size: int = None, encoding: str = "utf-8"):
        if not size:
            size = len(string) + 1
        return super().write(
            struct.pack(f"{self.endian_char()}{size}s", string.encode(encoding))
        )

    # NAVIGATION

    def align_to(self, alignment: int, char: bytes = b"\x00"):
        if alignment <= 0:
            raise Exception("Not possible")
        while self.tell() % alignment:
            super().write(char)

    # RESERVE, FILL

    def reserve(self, name: str, struct_type: str, size: int):
        name = f"{name}:{struct_type}"
        if name in self.reservations:
            raise Exception(f"Key already reserved: {name}")

        self.reservations[name] = self.tell()
        for _ in range(size):
            self.write_uint8(UInt8(0xFE))

    def fill(self, name: str, struct_type: str):
        name = f"{name}:{struct_type}"
        if not (name in self.reservations):
            raise Exception(f"Key not reserved: {name}")

        return self.reservations.pop(name)

    def reserve_int8(self, name: str):
        self.reserve(name, "i8", 1)

    def fill_int8(self, name: str, value: Int8):
        self.step_in(self.fill(name, "i8"))
        self.write_int8(value)
        self.step_out()

    def reserve_uint8(self, name: str):
        self.reserve(name, "u8", 1)

    def fill_uint8(self, name: str, value: UInt8):
        self.step_in(self.fill(name, "u8"))
        self.write_uint8(value)
        self.step_out()

    def reserve_int16(self, name: str):
        self.reserve(name, "i16", 2)

    def fill_int16(self, name: str, value: Int16):
        self.step_in(self.fill(name, "i16"))
        self.write_int16(value)
        self.step_out()

    def reserve_uint16(self, name: str):
        self.reserve(name, "u16", 2)

    def fill_uint16(self, name: str, value: UInt16):
        self.step_in(self.fill(name, "u16"))
        self.write_uint16(value)
        self.step_out()

    def reserve_int32(self, name: str):
        self.reserve(name, "i32", 4)

    def fill_int32(self, name: str, value: Int32):
        self.step_in(self.fill(name, "i32"))
        self.write_int32(value)
        self.step_out()

    def reserve_uint32(self, name: str):
        self.reserve(name, "u32", 4)

    def fill_uint32(self, name: str, value: UInt32):
        self.step_in(self.fill(name, "u32"))
        self.write_uint32(value)
        self.step_out()

    def reserve_int64(self, name: str):
        self.reserve(name, "i64", 8)

    def fill_int64(self, name: str, value: Int64):
        self.step_in(self.fill(name, "i64"))
        self.write_int64(value)
        self.step_out()

    def reserve_uint64(self, name: str):
        self.reserve(name, "u64", 8)

    def fill_uint64(self, name: str, value: UInt64):
        self.step_in(self.fill(name, "u64"))
        self.write_uint64(value)
        self.step_out()

    def reserve_float32(self, name: str):
        self.reserve(name, "f32", 4)

    def fill_float32(self, name: str, value: Float32):
        self.step_in(self.fill(name, "f32"))
        self.write_float32(value)
        self.step_out()

    def reserve_float64(self, name: str):
        self.reserve(name, "f64", 8)

    def fill_float64(self, name: str, value: Float64):
        self.step_in(self.fill(name, "f64"))
        self.write_float64(value)
        self.step_out()
