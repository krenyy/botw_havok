__all__ = ("BinaryWriter",)

import struct
from typing import Dict

import numpy as np

from .base import BinaryBase
from .types import *


class BinaryWriter(BinaryBase):
    reservations: Dict[str, UInt32]

    def __init__(self, initial_bytes=None, big_endian: bool = None):
        super().__init__(initial_bytes=initial_bytes, big_endian=big_endian)

        self.reservations = {}

    # WRITE

    def write_int8(self, num: Int8):
        return self.write(np.array([num], dtype=f"{self.endian_char()}b").tobytes())

    def write_uint8(self, num: UInt8):
        return self.write(np.array([num], dtype=f"{self.endian_char()}B").tobytes())

    def write_int16(self, num: Int16):
        return self.write(np.array([num], dtype=f"{self.endian_char()}h").tobytes())

    def write_uint16(self, num: UInt16):
        return self.write(np.array([num], dtype=f"{self.endian_char()}H").tobytes())

    def write_int32(self, num: Int32):
        return self.write(np.array([num], dtype=f"{self.endian_char()}i").tobytes())

    def write_uint32(self, num: UInt32):
        return self.write(np.array([num], dtype=f"{self.endian_char()}I").tobytes())

    def write_int64(self, num: Int64):
        return self.write(np.array([num], dtype=f"{self.endian_char()}q").tobytes())

    def write_uint64(self, num: UInt64):
        return self.write(np.array([num], dtype=f"{self.endian_char()}Q").tobytes())

    def write_float16(self, num: Float16):
        return self.write(np.array([num], dtype=f"{self.endian_char()}f2").tobytes())

    def write_float32(self, num: Float32):
        return self.write(np.array([num], dtype=f"{self.endian_char()}f").tobytes())

    def write_float64(self, num: Float64):
        return self.write(np.array([num], dtype=f"{self.endian_char()}d").tobytes())

    def write_vector(self, v: Vector):
        return self.write(np.array(v, dtype=f"{self.endian_char()}f").tobytes())

    def write_matrix(self, matrix: Matrix):
        return [self.write_vector(v) for v in matrix]

    def write_string(self, string: str, size: int = None, encoding: str = "utf-8"):
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
        res_name = f"{name}:{struct_type}"
        if res_name in self.reservations:
            raise Exception(f"Key already reserved: {res_name}")

        self.reservations[res_name] = self.tell()
        for _ in range(size):
            self.write_uint8(UInt8(0xFE))

    def fill(self, name: str, struct_type: str):
        res_name = f"{name}:{struct_type}"
        if not (res_name in self.reservations):
            raise Exception(f"Key not reserved: {res_name}")

        return self.reservations.pop(res_name)

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
