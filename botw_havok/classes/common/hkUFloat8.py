from ...binary import BinaryReader, BinaryWriter


class hkUFloat8:
    value: int

    def deserialize(self, hk, br: BinaryReader):
        self.value = br.read_uint8()

    def serialize(self, hk, bw: BinaryWriter):
        bw.write_uint8(self.value)

    def asdict(self):
        return {"value": self.value}

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.value = d["value"]
        return inst
