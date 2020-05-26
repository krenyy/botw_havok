from typing import List
from typing import TYPE_CHECKING

from .hkcdStaticMeshTreeBase import hkcdStaticMeshTreeBase
from .hkpBvCompressedMeshShapeTreeDataRun import hkpBvCompressedMeshShapeTreeDataRun
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32, UInt64

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkcdStaticMeshTreehkcdStaticMeshTreeCommonConfigunsignedintunsignedlonglong1121hkpBvCompressedMeshShapeTreeDataRun(
    hkcdStaticMeshTreeBase
):
    packedVertices: List[UInt32]
    sharedVertices: List[UInt64]
    primitiveDataRuns: List[hkpBvCompressedMeshShapeTreeDataRun]

    _packedVerticesCount_offset: UInt32
    _sharedVerticesCount_offset: UInt32
    _primitiveDataRunsCount_offset: UInt32

    def __init__(self):
        super().__init__()

        self.packedVertices = []
        self.sharedVertices = []
        self.primitiveDataRuns = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        packedVerticesCount_offset = hkFile._assert_pointer(br)
        packedVerticesCount = hkFile._read_counter(br)

        sharedVerticesCount_offset = hkFile._assert_pointer(br)
        sharedVerticesCount = hkFile._read_counter(br)

        primitiveDataRunsCount_offset = hkFile._assert_pointer(br)
        primitiveDataRunsCount = hkFile._read_counter(br)

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
                    dataRun.deserialize(hkFile, br, obj)

            br.step_out()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        self._packedVerticesCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.packedVertices)))

        self._sharedVerticesCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.sharedVertices)))

        self._primitiveDataRunsCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.primitiveDataRuns)))

        # Arrays get written later

    def as_dict(self):
        d = super().as_dict()
        d.update(
            {
                "packedVertices": self.packedVertices,
                "sharedVertices": self.sharedVertices,
                "primitiveDataRuns": [
                    dataRun.as_dict() for dataRun in self.primitiveDataRuns
                ],
            }
        )

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().from_dict(d).__dict__)

        inst.packedVertices = [UInt32(i) for i in d["packedVertices"]]
        inst.sharedVertices = [UInt64(i) for i in d["sharedVertices"]]
        inst.primitiveDataRuns = [
            hkpBvCompressedMeshShapeTreeDataRun.from_dict(dataRun)
            for dataRun in d["primitiveDataRuns"]
        ]

        return inst
