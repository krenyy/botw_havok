from collections.abc import Iterable

from ...binary import BinaryReader, BinaryWriter

if False:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkObject:
    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        raise NotImplementedError("This method is meant to be overridden!")

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        raise NotImplementedError("This method is meant to be overridden!")

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
