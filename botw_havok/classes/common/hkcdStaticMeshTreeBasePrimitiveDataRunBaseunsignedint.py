from ...binary import BinaryReader, BinaryWriter

if False:
    from ...hk import HK


class hkcdStaticMeshTreeBasePrimitiveDataRunBaseunsignedint:
    value: int
    index: int
    count: int

    def deserialize(self, hk: "HK", br: BinaryReader, obj):
        self.value = br.read_uint32()
        self.index = br.read_uint8()
        self.count = br.read_uint8()

        br.align_to(4)

    def serialize(self, hk: "HK", bw: BinaryWriter):
        bw.write_uint32(self.value)
        bw.write_uint8(self.index)
        bw.write_uint8(self.count)

        bw.align_to(4)

    def asdict(self):
        return {
            "value": self.value,
            "index": self.index,
            "count": self.count,
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()

        inst.value = d["value"]
        inst.index = d["index"]
        inst.count = d["count"]

        return inst
