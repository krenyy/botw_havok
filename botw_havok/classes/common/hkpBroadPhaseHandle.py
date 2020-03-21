from ...binary import BinaryReader, BinaryWriter

if False:
    from ...hk import HK


class hkpBroadPhaseHandle:
    id: int

    def deserialize(self, hk: "HK", br: BinaryReader):
        self.id = br.read_uint32()

    def serialize(self, hk: "HK", bw: BinaryWriter):
        bw.write_uint32(self.id)

    def asdict(self):
        return {"id": self.id}

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()

        inst.id = d["id"]

        return inst
