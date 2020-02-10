__all__ = ("Havok",)

import json
from .hk import HK
from typing import List, Union
from io import BufferedIOBase
from .binary import BinaryReader, BinaryWriter
from .util import todict


class Havok:
    files: List[HK]

    def __init__(self, d: dict = None):
        self.files = []

        if d:
            self.files = [HK.fromdict(file) for file in d]

    def read(self, data: Union[str, BufferedIOBase], deserialize: bool):
        if isinstance(data, str):
            with open(data, "rb") as f:
                br = BinaryReader(f.read())
        elif isinstance(data, BufferedIOBase):
            br = BinaryReader(data.read())

        # ---------------------------------------

        while br.tell() != len(br.getvalue()):
            br = BinaryReader(br.read())
            hk = HK()
            hk.read(br, deserialize)
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

    def load(self, path: str):
        with open(path, "r") as f:
            data = json.load(f)

        self = self.__class__.fromdict(data)

    def dump(self, path: str):
        with open(path, "w") as f:
            return f.write(json.dumps(self.asdict(), indent=4))

    def asdict(self):
        files = []
        for file in self.files:
            files.append(todict(file))
        return files

    @classmethod
    def fromdict(cls, d: dict):
        return cls(d)

    def to_switch(self):
        for file in self.files:
            file.to_switch()

    def to_wiiu(self):
        for file in self.files:
            file.to_wiiu()

    def __repr__(self):
        return f"<Havok {[file for file in self.files]}>"
