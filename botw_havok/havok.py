__all__ = ("Havok",)

import json
from pathlib import Path
from typing import List, Union

import numpy as np
from oead import yaz0

from .binary import BinaryReader, BinaryWriter
from .hkfile import HKFile


def default(o):
    if isinstance(o, np.integer):
        return int(o)
    elif isinstance(o, np.floating):
        return float(o)


class Havok:
    path: Path

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

    def guess_extension(self) -> str:
        contents = self.files[0].data.contents

        if not contents:
            raise Exception("File needs to be deserialized!")

        root_class = contents[0]

        if root_class.hkClass == "StaticCompoundInfo":
            return ".hksc"

        elif root_class.hkClass == "hkRootLevelContainer":
            if root_class.namedVariants[0].className == "hkpPhysicsData":  # type: ignore
                return ".hkrb"
            elif root_class.namedVariants[0].className == "hkpRigidBody":  # type: ignore
                return ".hktmrb"
            elif root_class.namedVariants[0].className == "hclClothContainer":  # type: ignore
                return ".hkcl"
            elif root_class.namedVariants[0].className == "hkaAnimationContainer":  # type: ignore
                return ".hkrg"
            elif root_class.namedVariants[0].className == "hkaiNavMesh":  # type: ignore
                return ".hknm2"

        return ".hkx"

    def as_dict(self):
        return [file.as_dict() for file in self.files]

    @classmethod
    def from_bytes(cls, b: bytes, path: Path = None):
        inst = cls()

        if path:
            inst.path = path

        if b[0:4] == b"Yaz0":
            b = yaz0.decompress(b)

        br = BinaryReader(initial_bytes=b)

        while br.tell() != br.length():
            br = BinaryReader(initial_bytes=br.read())

            file = HKFile()
            file.read(br)

            inst.files.append(file)

        return inst

    @classmethod
    def from_file(cls, path: Union[Path, str]):
        with open(path, "rb") as f:
            return cls.from_bytes(f.read(), Path(path))

    def to_file(self, path: str):
        bw = BinaryWriter()

        for file in self.files:
            _bw = BinaryWriter(big_endian=file.header.endian == 0)
            file.serialize()
            file.write(_bw)
            bw.write(_bw.getvalue())

        with open(path, "wb") as f:
            return f.write(bw.getvalue())

    @classmethod
    def from_dict(cls, l: list, path: Path = None):
        inst = cls()

        if path:
            inst.path = path

        inst.files = [HKFile.from_dict(file) for file in l]

        return inst

    @classmethod
    def from_json(cls, path: Union[Path, str]):
        with open(path, "r") as f:
            return cls.from_dict(json.load(f), Path(path))

    def to_json(self, path: str, pretty_print: bool = False):
        with open(path, "w") as f:
            if pretty_print:
                return f.write(json.dumps(self.as_dict(), indent=4, default=default))
            else:
                return json.dump(self.as_dict(), f, default=default)

    def __repr__(self) -> str:
        return "<{} {}>".format(self.__class__.__name__, self.files)
