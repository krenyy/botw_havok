from collections.abc import Iterable
from typing import TYPE_CHECKING

from ..binary import BinaryReader, BinaryWriter

if TYPE_CHECKING:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class HKBaseClass:
    hkClass: str

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        # SPECIFIC HKCLASS BEHAVIOUR EXECUTES AFTER THIS

        self.hkClass = obj.hkClass.name

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        # SPECIFIC HKCLASS BEHAVIOUR EXECUTES BEFORE THIS

        obj.bytes = bw.getvalue()
        obj.size = len(obj.bytes)

    def assign_class(self, hkFile: "HKFile", obj: "HKObject"):
        obj.hkClass = hkFile.classnames.get(self.hkClass)

    def as_dict(self):
        return {"hkClass": self.hkClass}

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.hkClass = d["hkClass"]

        return inst

    def __eq__(self, value: object):
        if not isinstance(value, HKBaseClass):
            raise NotImplementedError()
        return hash(self) == hash(value)

    def __hash__(self):
        return hash(
            frozenset(
                [
                    value if not isinstance(value, Iterable) else frozenset(value)
                    for value in self.__dict__.values()
                ]
            )
        )
