from ...binary import BinaryReader, BinaryWriter

# from .hkpShapeKeyTableBlock import hkpShapeKeyTableBlock


if False:
    from ...hk import HK


class hkpShapeKeyTable:
    # lists: hkpShapeKeyTableBlock
    occupancyBitField: int

    def deserialize(self, hk: "HK", br: BinaryReader):
        hk._assert_pointer(br)  # 'lists' pointer

        self.occupancyBitField = br.read_uint32()

        if hk.header.padding_option:
            br.align_to(16)

    def serialize(self, hk: "HK", bw: BinaryWriter):
        hk._write_empty_pointer(bw)

        bw.write_uint32(self.occupancyBitField)

        if hk.header.padding_option:
            bw.align_to(16)

    def asdict(self):
        return {
            # "lists": self.lists.asdict(),
            "occupancyBitField": self.occupancyBitField,
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()

        # inst.lists = hkpShapeKeyTableBlock.fromdict(d['lists'])
        inst.occupancyBitField = d["occupancyBitField"]

        return inst
