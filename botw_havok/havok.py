__all__ = ("Havok",)

import json
from io import BytesIO
from typing import List

from .binary import BinaryReader, BinaryWriter
from .hkfile import HKFile

from oead import yaz0


class Havok:
    files: List[HKFile]

    def __init__(self):
        self.files = []

    def deserialize(self):
        for file in self.files:
            file.deserialize()

    def serialize(self):
        for file in self.files:
            file.serialize()

    def to_switch(self):
        for file in self.files:
            file.to_switch()

    def to_wiiu(self):
        for file in self.files:
            file.to_wiiu()

    def guess_extension(self):
        contents = self.files[0].data.contents

        if not contents:
            raise Exception("File needs to be deserialized!")

        if contents[0].hkClass == "StaticCompoundInfo":
            return "hksc"

        elif contents[0].hkClass == "hkRootLevelContainer":
            if contents[0].namedVariants[0].className == "hkpPhysicsData":
                return "hkrb"
            elif contents[0].namedVariants[0].className == "hkpRigidBody":
                return "hktmrb"
            elif contents[0].namedVariants[0].className == "hclClothContainer":
                return "hkcl"
            elif contents[0].namedVariants[0].className == "hkaAnimationContainer":
                return "hkrg"

        return "hkx"

    def as_dict(self):
        return [file.as_dict() for file in self.files]

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.files = [HKFile.from_dict(file) for file in d]

        return inst

    @classmethod
    def from_file(cls, path: str):
        with open(path, "rb") as f:
            return cls.from_bytes(f.read())

    @classmethod
    def from_bytes(cls, b: bytes):
        inst = cls()

        if b[0:4] == b"Yaz0":
            b = yaz0.decompress(b)

        br = BinaryReader(initial_bytes=b)

        while br.tell() != br.length():
            br = BinaryReader(initial_bytes=br.read())

            file = HKFile()
            file.read(br)

            inst.files.append(file)

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
            return cls.from_dict(json.load(f))

    def to_json(self, path: str, pretty_print: bool = False):
        with open(path, "w") as f:
            if pretty_print:
                return f.write(json.dumps(self.as_dict(), indent=4))
            else:
                return json.dump(self.as_dict(), f)

    def __repr__(self):
        return f"<{self.__class__.__name__} {[file for file in self.files]}>"
