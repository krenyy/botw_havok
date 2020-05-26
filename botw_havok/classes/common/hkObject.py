from collections.abc import Iterable
from typing import TYPE_CHECKING

from ...binary import BinaryReader, BinaryWriter

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkObject:
    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        raise NotImplementedError("This method is meant to be overridden!")

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        raise NotImplementedError("This method is meant to be overridden!")

    def as_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(d)
        return inst

    def __eq__(self, value: object):
        if not isinstance(value, hkObject):
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
