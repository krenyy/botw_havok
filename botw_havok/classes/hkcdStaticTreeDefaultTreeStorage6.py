from typing import TYPE_CHECKING

from .base import HKBaseClass
from .common.hkcdStaticTreeDefaultTreeStorage6 import (
    hkcdStaticTreeDefaultTreeStorage6 as _hkcdStaticTreeDefaultTreeStorage6,
)
from ..binary import BinaryReader, BinaryWriter
from ..container.util.localfixup import LocalFixup

if TYPE_CHECKING:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkcdStaticTreeDefaultTreeStorage6(
    HKBaseClass, _hkcdStaticTreeDefaultTreeStorage6
):
    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        HKBaseClass.deserialize(self, hkFile, br, obj)
        _hkcdStaticTreeDefaultTreeStorage6.deserialize(self, hkFile, br, obj)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        HKBaseClass.assign_class(self, hkFile, obj)
        _hkcdStaticTreeDefaultTreeStorage6.serialize(self, hkFile, bw, obj)

        if self.nodes:
            obj.local_fixups.append(LocalFixup(self._nodesCount_offset, bw.tell()))

            [node.serialize(hkFile, bw, obj) for node in self.nodes]
            bw.align_to(16)

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def as_dict(self):
        d = HKBaseClass.as_dict(self)
        d.update(_hkcdStaticTreeDefaultTreeStorage6.as_dict(self))

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()

        inst.__dict__.update(HKBaseClass.from_dict(d).__dict__)
        inst.__dict__.update(_hkcdStaticTreeDefaultTreeStorage6.from_dict(d).__dict__)

        return inst
