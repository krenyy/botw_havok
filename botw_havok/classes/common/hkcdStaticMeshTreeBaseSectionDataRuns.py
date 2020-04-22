from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32

if False:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkcdStaticMeshTreeBaseSectionDataRuns:
    data: UInt32

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.data = br.read_uint32()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_uint32(UInt32(self.data))

    def asdict(self):
        return {"data": self.data}

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()

        inst.data = d["data"]

        return inst
