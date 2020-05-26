from typing import List
from typing import TYPE_CHECKING

from .base import HKBaseClass
from .common.hkReferencedObject import hkReferencedObject
from .common.hkaiDirectedGraphExplicitCostEdge import hkaiDirectedGraphExplicitCostEdge
from .common.hkaiDirectedGraphExplicitCostNode import hkaiDirectedGraphExplicitCostNode
from .common.hkaiStreamingSet import hkaiStreamingSet
from ..binary import BinaryReader, BinaryWriter
from ..binary.types import Int32, UInt32, Vector4
from ..container.util.localfixup import LocalFixup

if TYPE_CHECKING:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkaiDirectedGraphExplicitCost(HKBaseClass, hkReferencedObject):
    positions: List[Vector4]
    nodes: List[hkaiDirectedGraphExplicitCostNode]
    edges: List[hkaiDirectedGraphExplicitCostEdge]
    nodeData: List[UInt32]
    edgeData: List[UInt32]
    nodeDataStriding: Int32
    edgeDataStriding: Int32
    streamingSets: List[hkaiStreamingSet]

    def __init__(self):
        HKBaseClass.__init__(self)
        hkReferencedObject.__init__(self)

        self.positions = []
        self.nodes = []
        self.edges = []
        self.nodeData = []
        self.edgeData = []
        self.streamingSets = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        HKBaseClass.deserialize(self, hkFile, br, obj)
        hkReferencedObject.deserialize(self, hkFile, br, obj)

        ###

        if hkFile.header.padding_option:
            br.align_to(16)

        positionsCount_offset = hkFile._assert_pointer(br)
        positionsCount = hkFile._read_counter(br)

        nodesCount_offset = hkFile._assert_pointer(br)
        nodesCount = hkFile._read_counter(br)

        edgesCount_offset = hkFile._assert_pointer(br)
        edgesCount = hkFile._read_counter(br)

        nodeDataCount_offset = hkFile._assert_pointer(br)
        nodeDataCount = hkFile._read_counter(br)

        edgeDataCount_offset = hkFile._assert_pointer(br)
        edgeDataCount = hkFile._read_counter(br)

        self.nodeDataStriding = br.read_int32()
        self.edgeDataStriding = br.read_int32()

        streamingSetsCount_offset = hkFile._assert_pointer(br)
        streamingSetsCount = hkFile._read_counter(br)

        for lfu in obj.local_fixups:
            br.step_in(lfu.dst)

            if lfu.src == positionsCount_offset:
                for _ in range(positionsCount):
                    self.positions.append(br.read_vector4())

            elif lfu.src == nodesCount_offset:
                for _ in range(nodesCount):
                    node = hkaiDirectedGraphExplicitCostNode()
                    node.deserialize(hkFile, br, obj)
                    self.nodes.append(node)

            elif lfu.src == edgesCount_offset:
                for _ in range(edgesCount):
                    edge = hkaiDirectedGraphExplicitCostEdge()
                    edge.deserialize(hkFile, br, obj)
                    self.edges.append(edge)

            elif lfu.src == nodeDataCount_offset:
                for _ in range(nodeDataCount):
                    self.nodeData.append(br.read_uint32())

            elif lfu.src == edgeDataCount_offset:
                for _ in range(edgeDataCount):
                    self.edgeData.append(br.read_uint32())

            elif lfu.src == streamingSetsCount_offset:
                for _ in range(streamingSetsCount):
                    streamingSet = hkaiStreamingSet()
                    streamingSet.deserialize(hkFile, br, obj)
                    self.streamingSets.append(streamingSet)

            br.step_out()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        HKBaseClass.assign_class(self, hkFile, obj)
        hkReferencedObject.serialize(self, hkFile, bw, obj)

        ###

        if hkFile.header.padding_option:
            bw.align_to(16)

        positionsCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, len(self.positions))

        nodesCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, len(self.nodes))

        edgesCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, len(self.edges))

        nodeDataCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, len(self.nodeData))

        edgeDataCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, len(self.edgeData))

        bw.write_int32(self.nodeDataStriding)
        bw.write_int32(self.edgeDataStriding)

        streamingSetsCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, len(self.streamingSets))
        bw.align_to(16)

        # Positions
        if self.positions:
            obj.local_fixups.append(LocalFixup(positionsCount_offset, bw.tell()))

            for pos in self.positions:
                bw.write_vector(pos)

            bw.align_to(16)

        # Nodes
        if self.nodes:
            obj.local_fixups.append(LocalFixup(nodesCount_offset, bw.tell()))

            for node in self.nodes:
                node.serialize(hkFile, bw, obj)

            bw.align_to(16)

        # Edges
        if self.edges:
            obj.local_fixups.append(LocalFixup(edgesCount_offset, bw.tell()))

            for edge in self.edges:
                edge.serialize(hkFile, bw, obj)

            bw.align_to(16)

        # nodeData
        if self.nodeData:
            obj.local_fixups.append(LocalFixup(nodeDataCount_offset, bw.tell()))

            for nD in self.nodeData:
                bw.write_uint32(nD)

            bw.align_to(16)

        # edgeData
        if self.edgeData:
            obj.local_fixups.append(LocalFixup(nodeDataCount_offset, bw.tell()))

            for eD in self.edgeData:
                bw.write_uint32(eD)

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

        ###

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def as_dict(self):
        d = HKBaseClass.as_dict(self)
        d.update(hkReferencedObject.as_dict(self))
        d.update(
            {
                "positions": [v4.as_dict() for v4 in self.positions],
                "nodes": [node.as_dict() for node in self.nodes],
                "edges": [edge.as_dict() for edge in self.edges],
                "nodeData": self.nodeData,
                "edgeData": self.edgeData,
                "nodeDataStriding": self.nodeDataStriding,
                "edgeDataStriding": self.edgeDataStriding,
                "streamingSets": [sS.as_dict() for sS in self.streamingSets],
            }
        )

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBaseClass.from_dict(d).__dict__)
        inst.__dict__.update(hkReferencedObject.from_dict(d).__dict__)

        inst.positions = [Vector4.from_dict(v4) for v4 in d["positions"]]
        inst.nodes = [
            hkaiDirectedGraphExplicitCostNode.from_dict(node) for node in d["nodes"]
        ]
        inst.edges = [
            hkaiDirectedGraphExplicitCostEdge.from_dict(edge) for edge in d["edges"]
        ]
        inst.nodeData = d["nodeData"]
        inst.edgeData = d["edgeData"]
        inst.nodeDataStriding = d["nodeDataStriding"]
        inst.edgeDataStriding = d["edgeDataStriding"]
        inst.streamingSets = [
            hkaiStreamingSet.from_dict(sS) for sS in d["streamingSets"]
        ]

        return inst
