from io import BytesIO


class BinaryBase(BytesIO):
    big_endian: bool = False
    steps: list

    type_names = {
        "int8": "b",
        "uint8": "B",
        "int16": "h",
        "uint16": "H",
        "int32": "i",
        "uint32": "I",
        "int64": "q",
        "uint64": "Q",
        "float": "f",
        "double": "d",
        "char": "s",
    }

    def __init__(self, initial_bytes=None):
        super().__init__(initial_bytes=initial_bytes)
        self.steps = []

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
            raise Exception("Reader is already stepped all the way out")
        return self.seek_absolute(self.steps.pop())

    def endian_char(self):
        return ">" if self.big_endian else "<"

    def __repr__(self):
        return f"{self.__class__.__name__}(big_endian={self.big_endian})"
