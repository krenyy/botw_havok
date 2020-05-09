from io import BytesIO

import numpy as np

from .types import UInt32


class BinaryBase(BytesIO):
    big_endian: bool = False
    steps: list

    def __init__(self, initial_bytes=None, big_endian: bool = None):
        super().__init__(initial_bytes=initial_bytes)
        self.steps = []

        if big_endian:
            self.big_endian = big_endian

    def tell(self):
        return UInt32(super().tell())

    def length(self):
        return len(self.getvalue())

    def seek_absolute(self, offset: np.integer):
        return self.seek(offset, 0)

    def seek_relative(self, offset: np.integer):
        return self.seek(offset, 1)

    def step_in(self, offset: np.integer):
        self.steps.append(self.tell())
        return self.seek_absolute(offset)

    def step_in_relative(self, offset: np.integer):
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
