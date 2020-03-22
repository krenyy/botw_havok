__all__ = ("Havok",)

import json
from .hk import HK
from typing import List
from .binary import BinaryReader, BinaryWriter


class Havok:
    files: List[HK]

    def __init__(self, d: dict = None):
        self.files = []

    @classmethod
    def from_file(cls, path: str):
        inst = cls()

        with open(path, "rb") as f:
            br = BinaryReader(f.read())

        while br.tell() != len(br.getvalue()):
            br = BinaryReader(br.read())
            hk = HK()
            hk.read(br)
            inst.files.append(hk)

        return inst

    def to_file(self, path: str):
        bw = BinaryWriter()

        for file in self.files:
            _bw = BinaryWriter()
            _bw.big_endian = file.header.endian == 0
            file.serialize()
            file.write(_bw)
            bw.write(_bw.getvalue())

        # ---------------------------------------

        with open(path, "wb") as f:
            f.write(bw.getvalue())

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
