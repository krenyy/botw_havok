from typing import List

from ...binary import BinaryReader, BinaryWriter
from ..enums.ForceCollideOntoPpuReasons import ForceCollideOntoPpuReasons
from .hkpCollidable import hkpCollidable
from .hkpCollidableBoundingVolumeData import hkpCollidableBoundingVolumeData
from .hkpTypedBroadPhaseHandle import hkpTypedBroadPhaseHandle

if False:
    from ...hk import HK


class hkpLinkedCollidable(hkpCollidable):
    collisionEntries: List[None]

    def __init__(self):
        super().__init__()

        self.collisionEntries = []

    def deserialize(self, hk: "HK", br: BinaryReader, obj):
        super().deserialize(hk, br, obj)

        collisionEntriesCount_offset = br.tell()
        collisionEntriesCount = hk._read_counter(br)

    def serialize(self, hk: "HK", bw: BinaryWriter, obj):
        super().serialize(hk, bw, obj)

        collisionEntriesCount_offset = bw.tell()
        hk._write_counter(bw, len(self.collisionEntries))

    def asdict(self):
        d = super().asdict()

        d.update({"collisionEntries": self.collisionEntries})

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.collisionEntries = d["collisionEntries"]

        return inst
