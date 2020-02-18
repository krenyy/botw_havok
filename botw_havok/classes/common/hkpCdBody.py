from .hkpShape import hkpShape
from ...binary import BinaryReader, BinaryWriter

if False:
    from ...hk import HK


class hkpCdBody:
    shape: hkpShape = None
    shapeKey: int
    motion: None = None
    parent: "hkpCdBody" = None

    def deserialize(self, hk: "HK", br: BinaryReader):
        shape_offset = br.tell()
        hk._assert_pointer(br)  # Points to a hkpShape

        self.shapeKey = br.read_uint32()
        if hk.header.padding_option:
            br.align_to(8)

        hk._assert_pointer(br)  # motion, void
        hk._assert_pointer(br)  # points to parent hkpCdBody

    def serialize(self, hk: "HK", bw: BinaryWriter):
        shape_offset = bw.tell()
        hk._write_empty_pointer(bw)

        bw.write_uint32(self.shapeKey)
        if hk.header.padding_option:
            bw.align_to(16)

        hk._write_empty_pointer(bw)
        hk._write_empty_pointer(bw)

    def asdict(self):
        return {
            "shape": self.shape,
            "shapeKey": self.shapeKey,
            "motion": self.motion,
            "parent": self.parent,
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.shape = d["shape"]
        inst.shapeKey = d["shapeKey"]
        inst.motion = d["motion"]
        inst.parent = d["parent"]

        return inst
