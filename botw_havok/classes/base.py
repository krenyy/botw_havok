from ..binary import BinaryReader, BinaryWriter
from ..binary.types import String
from ..container.util.hkobject import HKObject

if False:
    from ..hkfile import HKFile


class HKBaseClass:
    hkClass: String

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: HKObject):
        # SPECIFIC HKCLASS BEHAVIOUR EXECUTES AFTER THIS

        self.hkClass = obj.hkClass.name

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: HKObject):
        # SPECIFIC HKCLASS BEHAVIOUR EXECUTES BEFORE THIS

        obj.bytes = bw.getvalue()
        obj.size = len(obj.bytes)

    def assign_class(self, hkFile: "HKFile", obj: "HKObject"):
        obj.hkClass = hkFile.classnames.get(self.hkClass)

    def asdict(self):
        return {"hkClass": self.hkClass}

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.hkClass = String(d["hkClass"])

        return inst
