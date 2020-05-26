from typing import List
from typing import TYPE_CHECKING

from .hkpCollidable import hkpCollidable
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpLinkedCollidable(hkpCollidable):
    collisionEntries: List[None]

    def __init__(self):
        super().__init__()

        self.collisionEntries = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        hkFile._assert_pointer(br)
        collisionEntriesCount = hkFile._read_counter(br)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.collisionEntries)))

    def as_dict(self):
        d = super().as_dict()

        d.update({"collisionEntries": self.collisionEntries})

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().from_dict(d).__dict__)

        inst.collisionEntries = d["collisionEntries"]

        return inst
