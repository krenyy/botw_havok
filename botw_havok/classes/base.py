from ..binary import BinaryReader, BinaryWriter
from typing import List
from ..container.sections.hkobject import HKObject


if False:
    from ..hk import HK


class HKBase:
    hkClass: str
    hkobj: HKObject

    def __init__(self):
        self.hkobj = HKObject()

    def deserialize(self, hk: "HK", obj: HKObject):
        self.hkobj = obj
        self.hkClass = self.hkobj.hkclass.name

    def assign_class(self, hk: "HK"):
        self.hkobj.hkclass = hk.classnames.get(self.hkClass)

    def serialize(self, hk: "HK", bw: BinaryWriter):
        self.hkobj.bytes = bw.getvalue()
        self.hkobj.size = len(self.hkobj.bytes)

    def asdict(self):
        return {"hkClass": self.hkClass}

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.hkClass = d["hkClass"]
        return inst
