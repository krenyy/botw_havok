__all__ = ("Havok",)

import json
from io import BytesIO
from typing import List

from .binary import BinaryReader, BinaryWriter
from .hkfile import HKFile


class Havok:
    files: List[HKFile]

    def __init__(self, d: dict = None):
        self.files = []

    @classmethod
    def from_file(cls, path: str):
        inst = cls()

        with open(path, "rb") as f:
            br = BinaryReader(f.read())

        while br.tell() != len(br.getvalue()):
            br = BinaryReader(br.read())
            file = HKFile()

            inst.files.append(file)

            file.read(br)

        return inst

    def to_file(self, path: str):
        bw = BinaryWriter()

        for file in self.files:
            _bw = BinaryWriter(big_endian=file.header.endian == 0)
            file.serialize()
            file.write(_bw)
            BytesIO.write(bw, _bw.getvalue())

        with open(path, "wb") as f:
            return f.write(bw.getvalue())

    @classmethod
    def from_json(cls, path: str):
        with open(path, "r") as f:
            return cls.fromdict(json.load(f))

    def to_json(self, path: str, pretty_print: bool = False):
        with open(path, "w") as f:
            if pretty_print:
                return f.write(json.dumps(self.asdict(), indent=4))
            else:
                return json.dump(self.asdict(), f)

    def deserialize(self):
        for file in self.files:
            file.deserialize()

    def serialize(self):
        for file in self.files:
            file.serialize()

    def asdict(self):
        return [file.asdict() for file in self.files]

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.files = [HKFile.fromdict(file) for file in d]

        return inst

    def to_switch(self):
        for file in self.files:
            file.to_switch()

    def to_wiiu(self):
        for file in self.files:
            file.to_wiiu()

    def __repr__(self):
        return f"<{self.__class__.__name__} {[file for file in self.files]}>"
