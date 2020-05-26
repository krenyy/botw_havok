from typing import List
from typing import TYPE_CHECKING

from .base import HKBaseClass
from .common.hkpConvexShape import hkpConvexShape
from ..binary import BinaryReader, BinaryWriter
from ..binary.types import Int32, Matrix, UInt8, UInt32, Vector4
from ..container.util.localfixup import LocalFixup

if TYPE_CHECKING:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkpConvexVerticesShape(HKBaseClass, hkpConvexShape):
    aabbHalfExtents: Vector4
    aabbCenter: Vector4

    rotatedVertices: List[Matrix]

    numVertices: Int32
    useSpuBuffer: bool

    planeEquations: Matrix

    # connectivity: hkpConvexVerticesConnectivity = None

    def __init__(self):
        HKBaseClass.__init__(self)
        hkpConvexShape.__init__(self)

        self.rotatedVertices = []
        self.planeEquations = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        HKBaseClass.deserialize(self, hkFile, br, obj)
        hkpConvexShape.deserialize(self, hkFile, br, obj)

        ###

        br.align_to(16)

        self.aabbHalfExtents = br.read_vector4()
        self.aabbCenter = br.read_vector4()

        rotatedVerticesCount_offset = hkFile._assert_pointer(br)
        rotatedVerticesCount = hkFile._read_counter(br)

        self.numVertices = br.read_int32()
        self.useSpuBuffer = bool(br.read_uint8())
        br.align_to(4)

        planeEquationsCount_offset = hkFile._assert_pointer(br)
        planeEquationsCount = hkFile._read_counter(br)

        connectivityPointer_offset = hkFile._assert_pointer(br)  # connectivity
        br.align_to(16)

        for lfu in obj.local_fixups:
            br.step_in(lfu.dst)

            if lfu.src == rotatedVerticesCount_offset:
                for _ in range(rotatedVerticesCount):
                    self.rotatedVertices.append(br.read_matrix(3))

            if lfu.src == planeEquationsCount_offset:
                self.planeEquations = br.read_matrix(planeEquationsCount)

            br.step_out()

        for gr in obj.global_references:
            if gr.src_rel_offset == connectivityPointer_offset:
                raise Exception(
                    "This 'hkpConvexVerticesShape' instance has 'connectivity' attribute, which hasn't been implemented yet"
                )

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        HKBaseClass.assign_class(self, hkFile, obj)
        hkpConvexShape.serialize(self, hkFile, bw, obj)

        ###

        bw.align_to(16)

        bw.write_vector(self.aabbHalfExtents)
        bw.write_vector(self.aabbCenter)

        rotatedVerticesCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.rotatedVertices)))

        bw.write_int32(self.numVertices)
        bw.write_uint8(UInt8(self.useSpuBuffer))
        bw.align_to(4)

        planeEquationsCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.planeEquations)))

        hkFile._write_empty_pointer(bw)  # 'connectivity'
        bw.align_to(16)

        ################
        # Write arrays #
        ################

        # rotatedVertices

        obj.local_fixups.append(LocalFixup(rotatedVerticesCount_offset, bw.tell()))

        [bw.write_matrix(rV) for rV in self.rotatedVertices]
        bw.align_to(16)

        # planeEquations

        obj.local_fixups.append(LocalFixup(planeEquationsCount_offset, bw.tell()))

        bw.write_matrix(self.planeEquations)

        ###

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def as_dict(self):
        d = HKBaseClass.as_dict(self)
        d.update(hkpConvexShape.as_dict(self))
        d.update(
            {
                "aabbHalfExtents": self.aabbHalfExtents.as_dict(),
                "aabbCenter": self.aabbCenter.as_dict(),
                "rotatedVertices": [rv.as_dict() for rv in self.rotatedVertices],
                "numVertices": self.numVertices,
                "useSpuBuffer": bool(self.useSpuBuffer),
                "planeEquations": self.planeEquations.as_dict(),
                # "connectivity": self.connectivity.as_dict(),
            }
        )

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBaseClass.from_dict(d).__dict__)
        inst.__dict__.update(hkpConvexShape.from_dict(d).__dict__)

        inst.aabbHalfExtents = Vector4.from_dict(d["aabbHalfExtents"])
        inst.aabbCenter = Vector4.from_dict(d["aabbCenter"])
        inst.rotatedVertices = [Matrix.from_dict(rv) for rv in d["rotatedVertices"]]
        inst.numVertices = d["numVertices"]
        inst.useSpuBuffer = bool(d["useSpuBuffer"])
        inst.planeEquations = Matrix.from_dict(d["planeEquations"])
        # inst.connectivity = hkpConvexVerticesConnectivity.from_dict(d["connectivity"])

        return inst
