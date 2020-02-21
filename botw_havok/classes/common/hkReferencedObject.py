from ...binary import BinaryReader, BinaryWriter
from .hkBaseObject import hkBaseObject

if False:
    from ...hk import HK


class hkReferencedObject(hkBaseObject):
    memSizeAndRefCount: int

    def deserialize(self, hk: "HK", br: BinaryReader):
        super().deserialize(hk, br)

        self.memSizeAndRefCount = br.read_uint32()

    def serialize(self, hk: "HK", bw: BinaryWriter):
        super().serialize(hk, bw)

        bw.write_uint32(self.memSizeAndRefCount)

    def asdict(self):
        return {"memSizeAndRefCount": self.memSizeAndRefCount}

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.memSizeAndRefCount = d["memSizeAndRefCount"]
        return inst
