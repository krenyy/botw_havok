from typing import List
from typing import TYPE_CHECKING

from .base import HKBaseClass
from .common.hkAabb import hkAabb
from .common.hkReferencedObject import hkReferencedObject
from .common.hkaiNavMeshEdge import hkaiNavMeshEdge
from .common.hkaiNavMeshFace import hkaiNavMeshFace
from .common.hkaiStreamingSet import hkaiStreamingSet
from ..binary import BinaryReader, BinaryWriter
from ..binary.types import Float64, Int32, UInt8, UInt64, Vector4
from ..container.util.localfixup import LocalFixup

if TYPE_CHECKING:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkaiNavMesh(HKBaseClass, hkReferencedObject):
    faces: List[hkaiNavMeshFace]
    edges: List[hkaiNavMeshEdge]
    vertices: List[Vector4]
    streamingSets: List[hkaiStreamingSet]
    faceData: List[Int32]
    edgeData: List[Int32]
    faceDataStriding: Int32
    edgeDataStriding: Int32
    flags: UInt8
    aabb: hkAabb
    erosionRadius: Float64
    userData: UInt64

    def __init__(self):
        HKBaseClass.__init__(self)
        hkReferencedObject.__init__(self)

        self.faces = []
        self.edges = []
        self.vertices = []
        self.streamingSets = []
        self.faceData = []
        self.edgeData = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        HKBaseClass.deserialize(self, hkFile, br, obj)
        hkReferencedObject.deserialize(self, hkFile, br, obj)

        ###

        if hkFile.header.padding_option:
            br.align_to(16)

        facesCount_offset = hkFile._assert_pointer(br)
        facesCount = hkFile._read_counter(br)

        edgesCount_offset = hkFile._assert_pointer(br)
        edgesCount = hkFile._read_counter(br)

        verticesCount_offset = hkFile._assert_pointer(br)
        verticesCount = hkFile._read_counter(br)

        streamingSetsCount_offset = hkFile._assert_pointer(br)
        streamingSetsCount = hkFile._read_counter(br)

        faceDataCount_offset = hkFile._assert_pointer(br)
        faceDataCount = hkFile._read_counter(br)

        edgeDataCount_offset = hkFile._assert_pointer(br)
        edgeDataCount = hkFile._read_counter(br)

        self.faceDataStriding = br.read_int32()
        self.edgeDataStriding = br.read_int32()

        self.flags = br.read_uint8()
        br.align_to(16)

        self.aabb = hkAabb()
        self.aabb.deserialize(hkFile, br, obj)

        self.erosionRadius = br.read_float64()
        self.userData = br.read_uint64()

        for lfu in obj.local_fixups:
            br.step_in(lfu.dst)

            if lfu.src == facesCount_offset:
                for _ in range(facesCount):
                    face = hkaiNavMeshFace()
                    face.deserialize(hkFile, br, obj)
                    self.faces.append(face)

            elif lfu.src == edgesCount_offset:
                for _ in range(edgesCount):
                    edge = hkaiNavMeshEdge()
                    edge.deserialize(hkFile, br, obj)
                    self.edges.append(edge)

            elif lfu.src == verticesCount_offset:
                for _ in range(verticesCount):
                    self.vertices.append(br.read_vector4())

            elif lfu.src == streamingSetsCount_offset:
                for _ in range(streamingSetsCount):
                    streamingSet = hkaiStreamingSet()
                    streamingSet.deserialize(hkFile, br, obj)
                    self.streamingSets.append(streamingSet)

            elif lfu.src == faceDataCount_offset:
                for _ in range(faceDataCount):
                    self.faceData.append(br.read_int32())

            elif lfu.src == edgeDataCount_offset:
                for _ in range(edgeDataCount):
                    self.edgeData.append(br.read_int32())

            br.step_out()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        HKBaseClass.assign_class(self, hkFile, obj)
        hkReferencedObject.serialize(self, hkFile, bw, obj)

        ###

        if hkFile.header.padding_option:
            bw.align_to(16)

        facesCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, len(self.faces))

        edgesCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, len(self.edges))

        verticesCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, len(self.vertices))

        streamingSetsCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, len(self.streamingSets))

        faceDataCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, len(self.faceData))

        edgeDataCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, len(self.edgeData))

        bw.write_uint32(self.faceDataStriding)
        bw.write_uint32(self.edgeDataStriding)

        bw.write_uint8(self.flags)
        bw.align_to(16)

        self.aabb.serialize(hkFile, bw, obj)

        bw.write_float64(self.erosionRadius)
        bw.write_uint64(self.userData)

        # Faces
        if self.faces:
            obj.local_fixups.append(LocalFixup(facesCount_offset, bw.tell()))

            for face in self.faces:
                face.serialize(hkFile, bw, obj)

            bw.align_to(16)

        # Edges
        if self.faces:
            obj.local_fixups.append(LocalFixup(edgesCount_offset, bw.tell()))

            for edge in self.edges:
                edge.serialize(hkFile, bw, obj)

            bw.align_to(16)

        # Vertices
        if self.vertices:
            obj.local_fixups.append(LocalFixup(verticesCount_offset, bw.tell()))

            for vtx in self.vertices:
                bw.write_vector(vtx)

            bw.align_to(16)

        # Streaming sets
        if self.streamingSets:
            obj.local_fixups.append(LocalFixup(streamingSetsCount_offset, bw.tell()))

            for streamingSet in self.streamingSets:
                streamingSet.serialize(hkFile, bw, obj)

            bw.align_to(16)

            for streamingSet in self.streamingSets:
                if streamingSet.meshConnections:
                    obj.local_fixups.append(
                        LocalFixup(streamingSet._meshConnectionsCount_offset, bw.tell())
                    )

                    for meshConnection in streamingSet.meshConnections:
                        meshConnection.serialize(hkFile, bw, obj)

                    bw.align_to(16)

                if streamingSet.graphConnections:
                    obj.local_fixups.append(
                        LocalFixup(
                            streamingSet._graphConnectionsCount_offset, bw.tell()
                        )
                    )

                    for graphConnection in streamingSet.graphConnections:
                        graphConnection.serialize(hkFile, bw, obj)

                    bw.align_to(16)

                if streamingSet.volumeConnections:
                    obj.local_fixups.append(
                        LocalFixup(
                            streamingSet._volumeConnectionsCount_offset, bw.tell()
                        )
                    )

                    for volumeConnection in streamingSet.volumeConnections:
                        volumeConnection.serialize(hkFile, bw, obj)

                    bw.align_to(16)

        # faceData
        if self.faceData:
            obj.local_fixups.append(LocalFixup(faceDataCount_offset, bw.tell()))

            for fD in self.faceData:
                bw.write_int32(fD)

            bw.align_to(16)

        # edgeData
        if self.edgeData:
            obj.local_fixups.append(LocalFixup(edgeDataCount_offset, bw.tell()))

            for eD in self.edgeData:
                bw.write_int32(eD)

            bw.align_to(16)

        ###

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def as_dict(self):
        d = HKBaseClass.as_dict(self)
        d.update(hkReferencedObject.as_dict(self))
        d.update(
            {
                "faces": [face.as_dict() for face in self.faces],
                "edges": [edge.as_dict() for edge in self.edges],
                "vertices": [vtx.as_dict() for vtx in self.vertices],
                "streamingSets": [sS.as_dict() for sS in self.streamingSets],
                "faceData": self.faceData,
                "edgeData": self.edgeData,
                "faceDataStriding": self.faceDataStriding,
                "edgeDataStriding": self.edgeDataStriding,
                "flags": self.flags,
                "aabb": self.aabb.as_dict(),
                "erosionRadius": self.erosionRadius,
                "userData": self.userData,
            }
        )

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBaseClass.from_dict(d).__dict__)
        inst.__dict__.update(hkReferencedObject.from_dict(d).__dict__)

        inst.faces = [hkaiNavMeshFace.from_dict(face) for face in d["faces"]]
        inst.edges = [hkaiNavMeshEdge.from_dict(edge) for edge in d["edges"]]
        inst.vertices = [Vector4.from_dict(vtx) for vtx in d["vertices"]]
        inst.streamingSets = [
            hkaiStreamingSet.from_dict(sS) for sS in d["streamingSets"]
        ]
        inst.faceData = d["faceData"]
        inst.edgeData = d["edgeData"]
        inst.faceDataStriding = d["faceDataStriding"]
        inst.edgeDataStriding = d["edgeDataStriding"]
        inst.flags = d["flags"]
        inst.aabb = hkAabb.from_dict(d["aabb"])
        inst.erosionRadius = d["erosionRadius"]
        inst.userData = d["userData"]

        return inst
