from ...binary import BinaryReader, BinaryWriter

if False:
    from ...hk import HK


class hkBaseObject:
    def deserialize(self, hk: "HK", br: BinaryReader):
        hk._assert_pointer(br)

    def serialize(self, hk: "HK", bw: BinaryWriter):
        hk._write_empty_pointer(bw)

    def __repr__(self):
        return f"{self.__class__.__name__}()"
