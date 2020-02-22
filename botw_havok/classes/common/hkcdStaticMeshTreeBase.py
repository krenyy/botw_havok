from typing import List

from ..base import BinaryReader, BinaryWriter
from .hkcdStaticMeshTreeBasePrimitive import hkcdStaticMeshTreeBasePrimitive
from .hkcdStaticMeshTreeBaseSection import hkcdStaticMeshTreeBaseSection
from .hkcdStaticTreeTreehkcdStaticTreeDynamicStorage5 import (
    hkcdStaticTreeTreehkcdStaticTreeDynamicStorage5,
)

if False:
    from ...hk import HK
    from ...container.sections.hkobject import HKObject


class hkcdStaticMeshTreeBase(hkcdStaticTreeTreehkcdStaticTreeDynamicStorage5):
    numPrimitiveKeys: int
    bitsPerKey: int
    maxKeyValue: int

    _sectionsCount_offset: int
    _primitivesCount_offset: int
    _sharedVerticesIndexCount_offset: int

    sections: List[hkcdStaticMeshTreeBaseSection]
    primitives: List[hkcdStaticMeshTreeBasePrimitive]
    sharedVerticesIndex: List[int]

    def __init__(self):
        super().__init__()

        self.sections = []
        self.primitives = []
        self.sharedVerticesIndex = []

    def deserialize(self, hk: "HK", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hk, br, obj)

        self.numPrimitiveKeys = br.read_int32()
        self.bitsPerKey = br.read_int32()
        self.maxKeyValue = br.read_uint32()

        if hk.header.padding_option:
            br.align_to(16)

        sectionsCount_offset = br.tell()
        sectionsCount = hk._read_counter(br)

        primitivesCount_offset = br.tell()
        primitivesCount = hk._read_counter(br)

        sharedVerticesIndexCount_offset = br.tell()
        sharedVerticesIndexCount = hk._read_counter(br)

        for lfu in obj.local_fixups:
            br.step_in(lfu.dst)

            if lfu.src == sectionsCount_offset:
                for _ in range(sectionsCount):
                    section = hkcdStaticMeshTreeBaseSection()
                    self.sections.append(section)
                    section.deserialize(hk, br, obj)

            if lfu.src == primitivesCount_offset:
                for _ in range(primitivesCount):
                    primitive = hkcdStaticMeshTreeBasePrimitive()
                    self.primitives.append(primitive)
                    primitive.deserialize(hk, br, obj)

            if lfu.src == sharedVerticesIndexCount_offset:
                for _ in range(sharedVerticesIndexCount):
                    self.sharedVerticesIndex.append(br.read_uint16())

            br.step_out()

    def serialize(self, hk: "HK", bw: BinaryWriter):
        super().serialize(hk, bw)

        bw.write_int32(self.numPrimitiveKeys)
        bw.write_int32(self.bitsPerKey)
        bw.write_uint32(self.maxKeyValue)

        if hk.header.padding_option:
            bw.align_to(16)

        self._sectionsCount_offset = bw.tell()
        hk._write_counter(bw, len(self.sections))

        self._primitivesCount_offset = bw.tell()
        hk._write_counter(bw, len(self.primitives))

        self._sharedVerticesIndexCount_offset = bw.tell()
        hk._write_counter(bw, len(self.sharedVerticesIndex))

        # Arrays get written later

    def asdict(self):
        d = super().asdict()
        d.update(
            {
                "numPrimitiveKeys": self.numPrimitiveKeys,
                "bitsPerKey": self.bitsPerKey,
                "maxKeyValue": self.maxKeyValue,
                "sections": [section.asdict() for section in self.sections],
                "primitives": [primitive.asdict() for primitive in self.primitives],
                "sharedVerticesIndex": self.sharedVerticesIndex,
            }
        )
        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.numPrimitiveKeys = d["numPrimitiveKeys"]
        inst.bitsPerKey = d["bitsPerKey"]
        inst.maxKeyValue = d["maxKeyValue"]
        inst.sections = [
            hkcdStaticMeshTreeBaseSection.fromdict(section) for section in d["sections"]
        ]
        inst.primitives = [
            hkcdStaticMeshTreeBasePrimitive.fromdict(primitive)
            for primitive in d["primitives"]
        ]
        inst.sharedVerticesIndex = d["sharedVerticesIndex"]

        return inst
