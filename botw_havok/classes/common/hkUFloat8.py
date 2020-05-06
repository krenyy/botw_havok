from ...binary.types import UInt8
from ...binary import BinaryReader, BinaryWriter


class hkUFloat8:
    value: UInt8

    def deserialize(self, br: BinaryReader):
        self.value = br.read_uint8()

    def serialize(self, bw: BinaryWriter):
        bw.write_uint8(self.value)

    def as_dict(self):
        return {"value": self.value}

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.value = d["value"]

        return inst
