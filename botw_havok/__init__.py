__all__ = ("Havok",)

import json
from .hk import HK
from typing import List, Union
from io import BufferedIOBase
from .binary import BinaryReader, BinaryWriter


class Havok:
    files: List[HK]

    def __init__(self, d: dict = None):
        self.files = []

    def read(self, data: Union[str, BufferedIOBase]):
        if isinstance(data, str):
            with open(data, "rb") as f:
                br = BinaryReader(f.read())
        elif isinstance(data, BufferedIOBase):
            br = BinaryReader(data.read())
        else:
            raise NotImplementedError("Invalid type passed!")

        # ---------------------------------------

        while br.tell() != len(br.getvalue()):
            br = BinaryReader(br.read())
            hk = HK()
            hk.read(br)
            self.files.append(hk)

    def write(self, data: Union[str, BufferedIOBase]):
        bw = BinaryWriter()

        for file in self.files:
            _bw = BinaryWriter()
            _bw.big_endian = file.header.endian == 0
            file.write(_bw)
            bw.write(_bw.getvalue())

        # ---------------------------------------

        if isinstance(data, str):
            with open(data, "wb") as f:
                f.write(bw.getvalue())
        elif isinstance(data, BufferedIOBase):
            data.write(bw.getvalue())

    @classmethod
    def load(cls, path: str):
        with open(path, "r") as f:
            return cls.fromdict(json.load(f))

    def dump(self, path: str):
        [file.deserialize() for file in self.files if not file.data.contents]

        with open(path, "w") as f:
            return f.write(json.dumps(self.asdict(), indent=4))

    def deserialize(self):
        for file in self.files:
            file.data.deserialize(file)

    def serialize(self):
        for file in self.files:
            file.data.serialize(file)

    def asdict(self):
        return [file.asdict() for file in self.files]

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.files = [HK.fromdict(file) for file in d]

        return inst

    def to_switch(self):
        for file in self.files:
            file.to_switch()

    def to_wiiu(self):
        for file in self.files:
            file.to_wiiu()

    def __repr__(self):
        return f"<{self.__class__.__name__} {[file for file in self.files]}>"
