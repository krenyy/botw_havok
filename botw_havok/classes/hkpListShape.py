from typing import List
from typing import TYPE_CHECKING

from .base import HKBaseClass
from .common.hkpListShapeChildInfo import hkpListShapeChildInfo
from .common.hkpShapeCollection import hkpShapeCollection
from ..binary import BinaryReader, BinaryWriter
from ..binary.types import UInt16, UInt32, Vector4
from ..container.util.localfixup import LocalFixup

if TYPE_CHECKING:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkpListShape(HKBaseClass, hkpShapeCollection):
    childInfo: List[hkpListShapeChildInfo]
    flags: UInt16
    numDisabledChildren: UInt16
    aabbHalfExtents: Vector4
    aabbCenter: Vector4
    enabledChildren: List[UInt32]

    def __init__(self):
        self.childInfo = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        HKBaseClass.deserialize(self, hkFile, br, obj)
        hkpShapeCollection.deserialize(self, hkFile, br, obj)

        ###

        childInfoCount_offset = hkFile._assert_pointer(br)
        childInfoCount = hkFile._read_counter(br)

        self.flags = br.read_uint16()
        self.numDisabledChildren = br.read_uint16()

        br.align_to(16)

        self.aabbHalfExtents = br.read_vector4()
        self.aabbCenter = br.read_vector4()
        self.enabledChildren = [br.read_uint32() for _ in range(8)]

        ###

        for lfu in obj.local_fixups:
            br.step_in(lfu.dst)

            if lfu.src == childInfoCount_offset:
                for _ in range(childInfoCount):
                    childInfo = hkpListShapeChildInfo()
                    childInfo.deserialize(hkFile, br, obj)

                    self.childInfo.append(childInfo)

            br.step_out()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        HKBaseClass.assign_class(self, hkFile, obj)
        hkpShapeCollection.serialize(self, hkFile, bw, obj)

        ###

        childInfoCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, len(self.childInfo))

        bw.write_uint16(self.flags)
        bw.write_uint16(self.numDisabledChildren)

        bw.align_to(16)

        bw.write_vector(self.aabbHalfExtents)
        bw.write_vector(self.aabbCenter)
        [bw.write_uint32(eC) for eC in self.enabledChildren]

        ###

        if self.childInfo:
            obj.local_fixups.append(LocalFixup(childInfoCount_offset, bw.tell()))

            for childInfo in self.childInfo:
                childInfo.serialize(hkFile, bw, obj)

        ###

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def as_dict(self):
        d = HKBaseClass.as_dict(self)
        d.update(hkpShapeCollection.as_dict(self))
        d.update(
            {
                "childInfo": [cI.as_dict() for cI in self.childInfo],
                "flags": self.flags,
                "numDisabledChildren": self.numDisabledChildren,
                "aabbHalfExtents": self.aabbHalfExtents.as_dict(),
                "aabbCenter": self.aabbCenter.as_dict(),
                "enabledChildren": self.enabledChildren,
            }
        )

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBaseClass.from_dict(d).__dict__)
        inst.__dict__.update(hkpShapeCollection.from_dict(d).__dict__)

        inst.childInfo = [hkpListShapeChildInfo.from_dict(cI) for cI in d["childInfo"]]
        inst.flags = d["flags"]
        inst.numDisabledChildren = d["numDisabledChildren"]
        inst.aabbHalfExtents = Vector4.from_dict(d["aabbHalfExtents"])
        inst.aabbCenter = Vector4.from_dict(d["aabbCenter"])
        inst.enabledChildren = d["enabledChildren"]

        return inst
