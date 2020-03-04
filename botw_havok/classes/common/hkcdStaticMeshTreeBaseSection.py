from typing import List
from ...util import Vector3

from ...binary import BinaryReader, BinaryWriter
from .hkcdStaticMeshTreeBaseSectionDataRuns import hkcdStaticMeshTreeBaseSectionDataRuns
from .hkcdStaticMeshTreeBaseSectionPrimitives import (
    hkcdStaticMeshTreeBaseSectionPrimitives,
)
from .hkcdStaticMeshTreeBaseSectionSharedVertices import (
    hkcdStaticMeshTreeBaseSectionSharedVertices,
)
from .hkcdStaticTreeTreehkcdStaticTreeDynamicStorage4 import (
    hkcdStaticTreeTreehkcdStaticTreeDynamicStorage4,
)

if False:
    from ...hk import HK
    from ...container.sections.hkobject import HKObject


class hkcdStaticMeshTreeBaseSection(hkcdStaticTreeTreehkcdStaticTreeDynamicStorage4):
    codecParms: List[Vector3]
    firstPackedVertex: int
    sharedVertices: hkcdStaticMeshTreeBaseSectionSharedVertices
    primitives: hkcdStaticMeshTreeBaseSectionPrimitives
    dataRuns: hkcdStaticMeshTreeBaseSectionDataRuns
    numPackedVertices: int
    numSharedIndices: int
    leafIndex: int
    page: int
    flags: int
    layerData: int
    unusedData: int

    def deserialize(self, hk: "HK", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hk, br, obj)

        self.codecParms = [br.read_vector3() for _ in range(2)]
        self.firstPackedVertex = br.read_uint32()

        self.sharedVertices = hkcdStaticMeshTreeBaseSectionSharedVertices()
        self.sharedVertices.deserialize(hk, br, obj)

        self.primitives = hkcdStaticMeshTreeBaseSectionPrimitives()
        self.primitives.deserialize(hk, br, obj)

        self.dataRuns = hkcdStaticMeshTreeBaseSectionDataRuns()
        self.dataRuns.deserialize(hk, br, obj)

        self.numPackedVertices = br.read_uint8()
        self.numSharedIndices = br.read_uint8()
        self.leafIndex = br.read_uint16()

        self.page = br.read_uint8()
        self.flags = br.read_uint8()
        self.layerData = br.read_uint8()
        self.unusedData = br.read_uint8()

    def serialize(self, hk: "HK", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hk, bw)

        [bw.write_vector3(cp) for cp in self.codecParms]
        bw.write_uint32(self.firstPackedVertex)

        self.sharedVertices.serialize(hk, bw, obj)
        self.primitives.serialize(hk, bw, obj)
        self.dataRuns.serialize(hk, bw, obj)

        bw.write_uint8(self.numPackedVertices)
        bw.write_uint8(self.numSharedIndices)
        bw.write_uint16(self.leafIndex)

        bw.write_uint8(self.page)
        bw.write_uint8(self.flags)
        bw.write_uint8(self.layerData)
        bw.write_uint8(self.unusedData)

    def asdict(self):
        d = super().asdict()
        d.update(
            {
                "codecParms": [cp.asdict() for cp in self.codecParms],
                "firstPackedVertex": self.firstPackedVertex,
                "sharedVertices": self.sharedVertices.asdict(),
                "primitives": self.primitives.asdict(),
                "dataRuns": self.dataRuns.asdict(),
                "numPackedVertices": self.numPackedVertices,
                "numSharedIndices": self.numSharedIndices,
                "leafIndex": self.leafIndex,
                "page": self.page,
                "flags": self.flags,
                "layerData": self.layerData,
                "unusedData": self.unusedData,
            }
        )

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.codecParms = [Vector3.fromdict(cp) for cp in d["codecParms"]]
        inst.firstPackedVertex = d["firstPackedVertex"]
        inst.sharedVertices = hkcdStaticMeshTreeBaseSectionSharedVertices.fromdict(
            d["sharedVertices"]
        )
        inst.primitives = hkcdStaticMeshTreeBaseSectionPrimitives.fromdict(
            d["primitives"]
        )
        inst.dataRuns = hkcdStaticMeshTreeBaseSectionDataRuns.fromdict(d["dataRuns"])
        inst.numPackedVertices = d["numPackedVertices"]
        inst.numSharedIndices = d["numSharedIndices"]
        inst.leafIndex = d["leafIndex"]
        inst.page = d["page"]
        inst.flags = d["flags"]
        inst.layerData = d["layerData"]
        inst.unusedData = d["unusedData"]

        return inst
