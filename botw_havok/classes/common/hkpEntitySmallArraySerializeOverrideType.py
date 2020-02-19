from ...binary import BinaryReader, BinaryWriter

if False:
    from ...hk import HK


class hkpEntitySmallArraySerializeOverrideType:
    # data: None = None
    size: int
    capacityAndFlags: int

    def deserialize(self, hk: "HK", br: BinaryReader):
        data_offset = br.tell()
        hk._assert_pointer(br)  # 'data' pointer

        self.size = br.read_uint16()
        self.capacityAndFlags = br.read_uint16()

        if hk.header.padding_option:
            br.align_to(8)

    def serialize(self, hk: "HK", bw: BinaryWriter):
        data_offset = bw.tell()
        hk._write_empty_pointer(bw)

        bw.write_uint16(self.size)
        bw.write_uint16(self.capacityAndFlags)

        if hk.header.padding_option:
            bw.align_to(8)

    def asdict(self):
        return {
            # "data": self.data,
            "size": self.size,
            "capacityAndFlags": self.capacityAndFlags,
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        # inst.data = d["data"]
        inst.size = d["size"]
        inst.capacityAndFlags = d["capacityAndFlags"]

        return inst
