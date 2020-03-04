__all__ = ("BinaryWriter",)


import struct
import typing

import numpy as np

from ..util import Matrix, Vector3, Vector4
from .base import BinaryBase


class BinaryWriter(BinaryBase):
    reservations: typing.Mapping[str, int]

    # WRITE

    def __init__(self, initial_bytes=None):
        super().__init__(initial_bytes=initial_bytes)
        self.reservations = {}

    def write_type(self, type: str, value) -> bytes:
        return self.write(
            struct.pack(f"{self.endian_char()}{self.type_names[type]}", value)
        )

    def write_int8(self, num: int) -> int:
        return self.write_type("int8", num)

    def write_uint8(self, num: int) -> int:
        return self.write_type("uint8", num)

    def write_int16(self, num: int) -> int:
        return self.write_type("int16", num)

    def write_uint16(self, num: int) -> int:
        return self.write_type("uint16", num)

    def write_int32(self, num: int) -> int:
        return self.write_type("int32", num)

    def write_uint32(self, num: int) -> int:
        return self.write_type("uint32", num)

    def write_int64(self, num: int) -> int:
        return self.write_type("int64", num)

    def write_uint64(self, num: int) -> int:
        return self.write_type("uint64", num)

    def write_floatu8(self, num: float) -> int:
        if num > 1 or num < 0:
            raise Exception("FloatU8 can only be between 0 and 1")
        return self.write_uint8(round((num * 0xFF) / 1))

    def write_half(self, num: float) -> int:
        return self.write(np.array([num], dtype=f"{self.endian_char()}f2").tobytes())

    def write_single(self, num: float) -> int:
        return self.write_type("float", num)

    def write_double(self, num: float) -> int:
        return self.write_type("double", num)

    def write_vector3(self, vector: Vector3) -> int:
        return self.write(struct.pack(f"{self.endian_char()}3f", *vector))

    def write_vector4(self, vector: Vector4) -> int:
        return self.write(struct.pack(f"{self.endian_char()}4f", *vector))

    def write_matrix(self, matrix: Matrix) -> list:
        return [self.write_vector4(v4) for v4 in matrix]

    def write_string(self, string: str, size: int = None) -> str:
        if isinstance(string, str):
            string = string.encode()
        if not size:
            size = len(string) + 1
        return self.write(struct.pack(f"{self.endian_char()}{size}s", string))

    # NAVIGATION

    def align_to(self, alignment: int, char=b"\x00"):
        if alignment <= 0:
            raise Exception("Not possible")
        while self.tell() % alignment:
            self.write(char)

    # RESERVE, FILL

    def reserve(self, name: str, struct_type: str, size: int):
        name = f"{name}:{struct_type}"
        if name in self.reservations:
            raise Exception(f"Key already reserved: {name}")

        self.reservations[name] = self.tell()
        for _ in range(size):
            self.write_uint8(0xFE)

    def fill(self, name: str, struct_type: str):
        name = f"{name}:{struct_type}"
        if not (name in self.reservations):
            raise Exception(f"Key not reserved: {name}")

        return self.reservations.pop(name)

    def reserve_uint8(self, name: str):
        self.reserve(name, "uint8", 1)

    def fill_uint8(self, name: str, value: int):
        self.step_in(self.fill(name, "uint8"))
        self.write_uint8(value)
        self.step_out()

    def reserve_int8(self, name: str):
        self.reserve(name, "int8", 1)

    def fill_int8(self, name: str, value: int):
        self.step_in(self.fill(name, "int8"))
        self.write_int8(value)
        self.step_out()

    def reserve_uint16(self, name: str):
        self.reserve(name, "uint16", 2)

    def fill_uint16(self, name: str, value: int):
        self.step_in(self.fill(name, "uint16"))
        self.write_uint16(value)
        self.step_out()

    def reserve_int16(self, name: str):
        self.reserve(name, "int16", 2)

    def fill_int16(self, name: str, value: int):
        self.step_in(self.fill(name, "int16"))
        self.write_int16(value)
        self.step_out()

    def reserve_uint32(self, name: str):
        self.reserve(name, "uint32", 4)

    def fill_uint32(self, name: str, value: int):
        self.step_in(self.fill(name, "uint32"))
        self.write_uint32(value)
        self.step_out()

    def reserve_int32(self, name: str):
        self.reserve(name, "int32", 4)

    def fill_int32(self, name: str, value: int):
        self.step_in(self.fill(name, "int32"))
        self.write_int32(value)
        self.step_out()

    def reserve_uint64(self, name: str):
        self.reserve(name, "uint64", 8)

    def fill_uint64(self, name: str, value: int):
        self.step_in(self.fill(name, "uint64"))
        self.write_uint64(value)
        self.step_out()

    def reserve_int64(self, name: str):
        self.reserve(name, "int64", 8)

    def fill_int64(self, name: str, value: int):
        self.step_in(self.fill(name, "int64"))
        self.write_int64(value)
        self.step_out()

    def reserve_single(self, name: str):
        self.reserve(name, "float", 4)

    def fill_single(self, name: str, value: int):
        self.step_in(self.fill(name, "float"))
        self.write_single(value)
        self.step_out()

    def reserve_double(self, name: str):
        self.reserve(name, "double", 8)

    def fill_double(self, name: str, value: int):
        self.step_in(self.fill(name, "double"))
        self.write_double(value)
        self.step_out()
