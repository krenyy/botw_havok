from io import BytesIO

from .types import UInt32


class BinaryBase(BytesIO):
    big_endian: bool = False
    steps: list

    struct_types = {
        "i8": "b",
        "i16": "h",
        "i32": "i",
        "i64": "q",
        "u8": "B",
        "u16": "H",
        "u32": "I",
        "u64": "Q",
        "f32": "f",
        "f64": "d",
        "string": "s",
    }

    def __init__(self, initial_bytes=None, big_endian: bool = None):
        super().__init__(initial_bytes=initial_bytes)
        self.steps = []

        if big_endian:
            self.big_endian = big_endian

    def tell(self):
        return UInt32(super().tell())

    def seek_absolute(self, offset: int):
        return self.seek(offset, 0)

    def seek_relative(self, offset: int):
        return self.seek(offset, 1)

    def step_in(self, offset: int):
        self.steps.append(self.tell())
        return self.seek_absolute(offset)

    def step_in_relative(self, offset: int):
        self.steps.append(self.tell())
        return self.seek_relative(offset)

    def step_out(self):
        if len(self.steps) == 0:
            raise Exception(
                f"{self.__class__.__name__} is already stepped all the way out"
            )
        return self.seek_absolute(self.steps.pop())

    def endian_char(self):
        return ">" if self.big_endian else "<"

    def __repr__(self):
        return f"{self.__class__.__name__}(big_endian={self.big_endian})"
