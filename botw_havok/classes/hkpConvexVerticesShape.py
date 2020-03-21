from typing import List

from ..binary import BinaryReader, BinaryWriter
from ..container.sections.util import LocalFixup
from ..util import Matrix, Vector4
from .base import HKBase
from .common.hkpConvexShape import hkpConvexShape

if False:
    from ..hk import HK


class hkpConvexVerticesShape(HKBase, hkpConvexShape):
    aabbHalfExtents: Vector4
    aabbCenter: Vector4

    rotatedVertices: List[Matrix]

    numVertices: int
    useSpuBuffer: bool

    planeEquations: Matrix

    # connectivity: hkpConvexVerticesConnectivity = None

    def __init__(self):
        HKBase.__init__(self)
        hkpConvexShape.__init__(self)

        self.rotatedVertices = []
        self.planeEquations = []

    def deserialize(self, hk: "HK", obj):
        HKBase.deserialize(self, hk, obj)

        br = BinaryReader(self.hkobj.bytes)
        br.big_endian = hk.header.endian == 0

        hkpConvexShape.deserialize(self, hk, br, obj)
        br.align_to(16)

        self.aabbHalfExtents = br.read_vector4()
        self.aabbCenter = br.read_vector4()

        rotatedVerticesCount_offset = br.tell()
        rotatedVerticesCount = hk._read_counter(br)

        self.numVertices = br.read_int32()
        self.useSpuBuffer = bool(br.read_uint8())
        br.align_to(4)  # TODO: Check if correct

        planeEquationsCount_offset = br.tell()
        planeEquationsCount = hk._read_counter(br)

        connectivityPointer_offset = br.tell()
        hk._assert_pointer(br)  # connectivity
        br.align_to(16)

        for lfu in self.hkobj.local_fixups:
            br.step_in(lfu.dst)

            if lfu.src == rotatedVerticesCount_offset:
                for _ in range(rotatedVerticesCount):
                    self.rotatedVertices.append(br.read_matrix(3))

            if lfu.src == planeEquationsCount_offset:
                self.planeEquations = br.read_matrix(planeEquationsCount)

            br.step_out()

        for gr in self.hkobj.global_references:
            if gr.src_rel_offset == connectivityPointer_offset:
                raise Exception(
                    "This 'hkpConvexVerticesShape' instance has 'connectivity' attribute, which hasn't been implemented yet"
                )

    def serialize(self, hk: "HK"):
        HKBase.assign_class(self, hk)

        bw = BinaryWriter()
        bw.big_endian = hk.header.endian == 0

        hkpConvexShape.serialize(self, hk, bw, self.hkobj)
        bw.align_to(16)

        bw.write_vector4(self.aabbHalfExtents)
        bw.write_vector4(self.aabbCenter)

        rotatedVerticesCount_offset = bw.tell()
        hk._write_counter(bw, len(self.rotatedVertices))

        bw.write_int32(self.numVertices)
        bw.write_uint8(int(self.useSpuBuffer))
        bw.align_to(4)  # TODO: Check if correct

        planeEquationsCount_offset = bw.tell()
        hk._write_counter(bw, len(self.planeEquations))

        connectivityPointer_offset = bw.tell()
        hk._write_empty_pointer(bw)  # connectivity
        bw.align_to(16)

        rotatedVertices_offset = bw.tell()
        for rv in self.rotatedVertices:
            bw.write_matrix(rv)
        bw.align_to(16)

        planeEquations_offset = bw.tell()
        bw.write_matrix(self.planeEquations)

        self.hkobj.local_fixups.extend(
            [
                LocalFixup(rotatedVerticesCount_offset, rotatedVertices_offset),
                LocalFixup(planeEquationsCount_offset, planeEquations_offset),
            ]
        )

        HKBase.serialize(self, hk, bw)

    def asdict(self):
        d = HKBase.asdict(self)
        d.update(hkpConvexShape.asdict(self))
        d.update(
            {
                "aabbHalfExtents": self.aabbHalfExtents.asdict(),
                "aabbCenter": self.aabbCenter.asdict(),
                "rotatedVertices": [rv.asdict() for rv in self.rotatedVertices],
                "numVertices": self.numVertices,
                "useSpuBuffer": self.useSpuBuffer,
                "planeEquations": self.planeEquations.asdict(),
                # "connectivity": self.connectivity.asdict(),
            }
        )

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBase.fromdict(d).__dict__)
        inst.__dict__.update(hkpConvexShape.fromdict(d).__dict__)

        inst.aabbHalfExtents = Vector4.fromdict(d["aabbHalfExtents"])
        inst.aabbCenter = Vector4.fromdict(d["aabbCenter"])
        inst.rotatedVertices = [Matrix.fromdict(rv) for rv in d["rotatedVertices"]]
        inst.numVertices = d["numVertices"]
        inst.useSpuBuffer = d["useSpuBuffer"]
        inst.planeEquations = Matrix.fromdict(d["planeEquations"])
        # inst.connectivity = hkpConvexVerticesConnectivity.fromdict(d["connectivity"])

        return inst
