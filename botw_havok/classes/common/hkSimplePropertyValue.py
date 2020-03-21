from ...binary import BinaryReader, BinaryWriter

if False:
    from ...hk import HK


class hkSimplePropertyValue:
    data: int

    def deserialize(self, hk: "HK", br: BinaryReader):
        self.data = br.read_uint64()

    def serialize(self, hk: "HK", bw: BinaryWriter):
        bw.write_uint64(self.data)

    def asdict(self):
        return {"data": self.data}

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.data = d["data"]

        return inst
