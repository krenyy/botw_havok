from typing import List

from ...binary import BinaryReader, BinaryWriter
from .hkcdStaticMeshTreeBase import hkcdStaticMeshTreeBase
from .hkpBvCompressedMeshShapeTreeDataRun import hkpBvCompressedMeshShapeTreeDataRun

if False:
    from ...hk import HK
    from ...container.sections.hkobject import HKObject


class hkcdStaticMeshTreehkcdStaticMeshTreeCommonConfigunsignedintunsignedlonglong1121hkpBvCompressedMeshShapeTreeDataRun(
    hkcdStaticMeshTreeBase
):
    _packedVerticesCount_offset: int
    _sharedVerticesCount_offset: int
    _primitiveDataRunsCount_offset: int

    packedVertices: List[int]
    sharedVertices: List[int]
    primitiveDataRuns: List[hkpBvCompressedMeshShapeTreeDataRun]

    def __init__(self):
        super().__init__()

        self.packedVertices = []
        self.sharedVertices = []
        self.primitiveDataRuns = []

    def deserialize(self, hk: "HK", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hk, br, obj)

        packedVerticesCount_offset = br.tell()
        packedVerticesCount = hk._read_counter(br)

        sharedVerticesCount_offset = br.tell()
        sharedVerticesCount = hk._read_counter(br)

        primitiveDataRunsCount_offset = br.tell()
        primitiveDataRunsCount = hk._read_counter(br)

        for lfu in obj.local_fixups:
            br.step_in(lfu.dst)

            if lfu.src == packedVerticesCount_offset:
                for _ in range(packedVerticesCount):
                    self.packedVertices.append(br.read_uint32())

            elif lfu.src == sharedVerticesCount_offset:
                for _ in range(sharedVerticesCount):
                    self.sharedVertices.append(br.read_uint64())

            elif lfu.src == primitiveDataRunsCount_offset:
                for _ in range(primitiveDataRunsCount):
                    dataRun = hkpBvCompressedMeshShapeTreeDataRun()
                    self.primitiveDataRuns.append(dataRun)
                    dataRun.deserialize(hk, br, obj)

            br.step_out()

    def serialize(self, hk: "HK", bw: BinaryWriter):
        super().serialize(hk, bw)

        self._packedVerticesCount_offset = bw.tell()
        hk._write_counter(bw, len(self.packedVertices))

        self._sharedVerticesCount_offset = bw.tell()
        hk._write_counter(bw, len(self.sharedVertices))

        self._primitiveDataRunsCount_offset = bw.tell()
        hk._write_counter(bw, len(self.primitiveDataRuns))

        # Array data gets written later

    def asdict(self):
        d = super().asdict()
        d.update(
            {
                "packedVertices": self.packedVertices,
                "sharedVertices": self.sharedVertices,
                "primitiveDataRuns": [
                    dataRun.asdict() for dataRun in self.primitiveDataRuns
                ],
            }
        )

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.packedVertices = d["packedVertices"]
        inst.sharedVertices = d["sharedVertices"]
        inst.primitiveDataRuns = [
            hkpBvCompressedMeshShapeTreeDataRun.fromdict(dataRun)
            for dataRun in d["primitiveDataRuns"]
        ]

        return inst
