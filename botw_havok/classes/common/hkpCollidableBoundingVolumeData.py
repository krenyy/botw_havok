from ...binary import BinaryWriter, BinaryReader
from typing import List


if False:
    from ...hk import HK


class hkpCollidableBoundingVolumeData:
    min: List[int]
    expansionMin: List[int]

    expansionShift: int

    max: List[int]
    expansionMax: List[int]

    numChildShapeAabbs: int
    capacityChildShapeAabbs: int
    # childShapeAabbs: None = None
    # childShapeKeys: None = None

    def deserialize(self, hk: "HK", br: BinaryReader):
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
        if hk.header.padding_option:
            br.align_to(8)

        # Empty pointers (?)
        hk._assert_pointer(br)  # childShapeAabbs
        hk._assert_pointer(br)  # childShapeKeys

    def serialize(self, hk: "HK", bw: BinaryWriter):
        [bw.write_uint32(m) for m in self.min]
        [bw.write_uint8(exm) for exm in self.expansionMin]

        bw.write_uint8(self.expansionShift)

        [bw.write_uint32(m) for m in self.max]
        [bw.write_uint8(exm) for exm in self.expansionMax]

        bw.write_uint8(0)

        # ----

        bw.write_uint16(self.numChildShapeAabbs)
        bw.write_uint16(self.capacityChildShapeAabbs)

        if hk.header.padding_option:
            bw.align_to(8)

        # Empty pointers
        hk._write_empty_pointer(bw)  # childShapeAabbs
        hk._write_empty_pointer(bw)  # childShapeKeys

    def asdict(self):
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
    def fromdict(cls, d: dict):
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
