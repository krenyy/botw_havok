from typing import List
from typing import TYPE_CHECKING

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
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt8, UInt16, UInt32, Vector3

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkcdStaticMeshTreeBaseSection(hkcdStaticTreeTreehkcdStaticTreeDynamicStorage4):
    codecParms: List[Vector3]
    firstPackedVertex: UInt32
    sharedVertices: hkcdStaticMeshTreeBaseSectionSharedVertices
    primitives: hkcdStaticMeshTreeBaseSectionPrimitives
    dataRuns: hkcdStaticMeshTreeBaseSectionDataRuns
    numPackedVertices: UInt8
    numSharedIndices: UInt8
    leafIndex: UInt16
    page: UInt8
    flags: UInt8
    layerData: UInt8
    unusedData: UInt8

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        self.codecParms = [br.read_vector3() for _ in range(2)]
        self.firstPackedVertex = br.read_uint32()

        # ---

        self.sharedVertices = hkcdStaticMeshTreeBaseSectionSharedVertices()
        self.sharedVertices.deserialize(hkFile, br, obj)

        self.primitives = hkcdStaticMeshTreeBaseSectionPrimitives()
        self.primitives.deserialize(hkFile, br, obj)

        self.dataRuns = hkcdStaticMeshTreeBaseSectionDataRuns()
        self.dataRuns.deserialize(hkFile, br, obj)

        # ---

        self.numPackedVertices = br.read_uint8()
        self.numSharedIndices = br.read_uint8()
        self.leafIndex = br.read_uint16()

        self.page = br.read_uint8()
        self.flags = br.read_uint8()
        self.layerData = br.read_uint8()
        self.unusedData = br.read_uint8()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        [bw.write_vector(cp) for cp in self.codecParms]
        bw.write_uint32(UInt32(self.firstPackedVertex))

        self.sharedVertices.serialize(hkFile, bw, obj)
        self.primitives.serialize(hkFile, bw, obj)
        self.dataRuns.serialize(hkFile, bw, obj)

        bw.write_uint8(UInt8(self.numPackedVertices))
        bw.write_uint8(UInt8(self.numSharedIndices))
        bw.write_uint16(UInt16(self.leafIndex))

        bw.write_uint8(UInt8(self.page))
        bw.write_uint8(UInt8(self.flags))
        bw.write_uint8(UInt8(self.layerData))
        bw.write_uint8(UInt8(self.unusedData))

    def as_dict(self):
        d = super().as_dict()
        d.update(
            {
                "codecParms": [cp.as_dict() for cp in self.codecParms],
                "firstPackedVertex": self.firstPackedVertex,
                "sharedVertices": self.sharedVertices.as_dict(),
                "primitives": self.primitives.as_dict(),
                "dataRuns": self.dataRuns.as_dict(),
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
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().from_dict(d).__dict__)

        inst.codecParms = [Vector3.from_dict(cp) for cp in d["codecParms"]]
        inst.firstPackedVertex = d["firstPackedVertex"]
        inst.sharedVertices = hkcdStaticMeshTreeBaseSectionSharedVertices.from_dict(
            d["sharedVertices"]
        )
        inst.primitives = hkcdStaticMeshTreeBaseSectionPrimitives.from_dict(
            d["primitives"]
        )
        inst.dataRuns = hkcdStaticMeshTreeBaseSectionDataRuns.from_dict(d["dataRuns"])
        inst.numPackedVertices = d["numPackedVertices"]
        inst.numSharedIndices = d["numSharedIndices"]
        inst.leafIndex = d["leafIndex"]
        inst.page = d["page"]
        inst.flags = d["flags"]
        inst.layerData = d["layerData"]
        inst.unusedData = d["unusedData"]

        return inst
