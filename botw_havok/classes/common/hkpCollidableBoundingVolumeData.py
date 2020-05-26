from typing import List
from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt8, UInt16, UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpCollidableBoundingVolumeData(hkObject):
    min: List[UInt32]
    expansionMin: List[UInt8]

    expansionShift: UInt8

    max: List[UInt32]
    expansionMax: List[UInt8]

    numChildShapeAabbs: UInt16
    capacityChildShapeAabbs: UInt16

    # childShapeAabbs: None = None
    # childShapeKeys: None = None

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.min = [br.read_uint32() for _ in range(3)]
        self.expansionMin = [br.read_uint8() for _ in range(3)]

        self.expansionShift = br.read_uint8()

        self.max = [br.read_uint32() for _ in range(3)]
        self.expansionMax = [br.read_uint8() for _ in range(3)]

        br.read_uint8()  # Padding

        # ----

        self.numChildShapeAabbs = br.read_uint16()
        self.capacityChildShapeAabbs = br.read_uint16()

        # Not entirely sure
        if hkFile.header.padding_option:
            br.align_to(8)

        # Empty pointers (?)
        hkFile._assert_pointer(br)  # childShapeAabbs
        hkFile._assert_pointer(br)  # childShapeKeys

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        [bw.write_uint32(UInt32(m)) for m in self.min]
        [bw.write_uint8(UInt8(exm)) for exm in self.expansionMin]

        bw.write_uint8(UInt8(self.expansionShift))

        [bw.write_uint32(UInt32(m)) for m in self.max]
        [bw.write_uint8(UInt8(exm)) for exm in self.expansionMax]

        bw.write_uint8(UInt8(0))

        # ----

        bw.write_uint16(self.numChildShapeAabbs)
        bw.write_uint16(self.capacityChildShapeAabbs)

        if hkFile.header.padding_option:
            bw.align_to(8)

        # Empty pointers
        hkFile._write_empty_pointer(bw)  # childShapeAabbs
        hkFile._write_empty_pointer(bw)  # childShapeKeys

    def as_dict(self):
        return {
            "min": self.min,
            "expansionMin": self.expansionMin,
            "expansionShift": self.expansionShift,
            "max": self.max,
            "expansionMax": self.expansionMax,
            "numChildShapeAabbs": self.numChildShapeAabbs,
            "capacityChildShapeAabbs": self.capacityChildShapeAabbs,
            # "childShapeAabbs": self.childShapeAabbs,
            # "childShapeKeys": self.childShapeKeys,
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.min = d["min"]
        inst.expansionMin = d["expansionMin"]
        inst.expansionShift = d["expansionShift"]
        inst.max = d["max"]
        inst.expansionMax = d["expansionMax"]
        inst.numChildShapeAabbs = d["numChildShapeAabbs"]
        inst.capacityChildShapeAabbs = d["capacityChildShapeAabbs"]
        # inst.childShapeAabbs = d["childShapeAabbs"]
        # inst.childShapeKeys = d["childShapeKeys"]

        return inst
