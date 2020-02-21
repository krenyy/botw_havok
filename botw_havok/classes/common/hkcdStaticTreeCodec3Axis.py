from typing import List

from ...binary import BinaryReader, BinaryWriter

if False:
    from ...hk import HK
    from ...container.sections.hkobject import HKObject


class hkcdStaticTreeCodec3Axis:
    xyz: List[int]

    def deserialize(self, hk: "HK", br: BinaryReader, obj: "HKObject"):
        self.xyz = [br.read_uint8() for _ in range(3)]

    def serialize(self, hk: "HK", bw: BinaryWriter, obj: "HKObject"):
        [bw.write_uint8(num) for num in self.xyz]

    def asdict(self):
        return {"xyz": self.xyz}

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()

        inst.xyz = d["xyz"]

        return inst
