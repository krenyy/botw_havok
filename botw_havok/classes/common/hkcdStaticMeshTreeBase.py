from typing import List
from typing import TYPE_CHECKING

from .hkcdStaticMeshTreeBasePrimitive import hkcdStaticMeshTreeBasePrimitive
from .hkcdStaticMeshTreeBaseSection import hkcdStaticMeshTreeBaseSection
from .hkcdStaticTreeTreehkcdStaticTreeDynamicStorage5 import (
    hkcdStaticTreeTreehkcdStaticTreeDynamicStorage5,
)
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Int32, UInt16, UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkcdStaticMeshTreeBase(hkcdStaticTreeTreehkcdStaticTreeDynamicStorage5):
    numPrimitiveKeys: Int32
    bitsPerKey: Int32
    maxKeyValue: UInt32

    sections: List[hkcdStaticMeshTreeBaseSection]
    primitives: List[hkcdStaticMeshTreeBasePrimitive]
    sharedVerticesIndex: List[UInt16]

    _sectionsCount_offset: UInt32
    _primitivesCount_offset: UInt32
    _sharedVerticesIndexCount_offset: UInt32

    def __init__(self):
        super().__init__()

        self.sections = []
        self.primitives = []
        self.sharedVerticesIndex = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        self.numPrimitiveKeys = br.read_int32()
        self.bitsPerKey = br.read_int32()
        self.maxKeyValue = br.read_uint32()

        if hkFile.header.padding_option:
            br.align_to(16)

        sectionsCount_offset = hkFile._assert_pointer(br)
        sectionsCount = hkFile._read_counter(br)

        primitivesCount_offset = hkFile._assert_pointer(br)
        primitivesCount = hkFile._read_counter(br)

        sharedVerticesIndexCount_offset = hkFile._assert_pointer(br)
        sharedVerticesIndexCount = hkFile._read_counter(br)

        for lfu in obj.local_fixups:
            br.step_in(lfu.dst)

            if lfu.src == sectionsCount_offset:
                for _ in range(sectionsCount):
                    section = hkcdStaticMeshTreeBaseSection()
                    self.sections.append(section)
                    section.deserialize(hkFile, br, obj)

            elif lfu.src == primitivesCount_offset:
                for _ in range(primitivesCount):
                    primitive = hkcdStaticMeshTreeBasePrimitive()
                    self.primitives.append(primitive)
                    primitive.deserialize(hkFile, br, obj)

            elif lfu.src == sharedVerticesIndexCount_offset:
                for _ in range(sharedVerticesIndexCount):
                    self.sharedVerticesIndex.append(br.read_uint16())

            br.step_out()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        bw.write_int32(Int32(self.numPrimitiveKeys))
        bw.write_int32(Int32(self.bitsPerKey))
        bw.write_uint32(UInt32(self.maxKeyValue))

        if hkFile.header.padding_option:
            bw.align_to(16)

        self._sectionsCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.sections)))

        self._primitivesCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.primitives)))

        self._sharedVerticesIndexCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.sharedVerticesIndex)))

        # Arrays get written later

    def as_dict(self):
        d = super().as_dict()
        d.update(
            {
                "numPrimitiveKeys": self.numPrimitiveKeys,
                "bitsPerKey": self.bitsPerKey,
                "maxKeyValue": self.maxKeyValue,
                "sections": [section.as_dict() for section in self.sections],
                "primitives": [primitive.as_dict() for primitive in self.primitives],
                "sharedVerticesIndex": self.sharedVerticesIndex,
            }
        )
        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().from_dict(d).__dict__)

        inst.numPrimitiveKeys = d["numPrimitiveKeys"]
        inst.bitsPerKey = d["bitsPerKey"]
        inst.maxKeyValue = d["maxKeyValue"]
        inst.sections = [
            hkcdStaticMeshTreeBaseSection.from_dict(section)
            for section in d["sections"]
        ]
        inst.primitives = [
            hkcdStaticMeshTreeBasePrimitive.from_dict(primitive)
            for primitive in d["primitives"]
        ]
        inst.sharedVerticesIndex = d["sharedVerticesIndex"]

        return inst
