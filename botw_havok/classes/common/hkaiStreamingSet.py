from typing import List
from typing import TYPE_CHECKING

from .hkObject import hkObject
from .hkaiStreamingSetGraphConnection import hkaiStreamingSetGraphConnection
from .hkaiStreamingSetNavMeshConnection import hkaiStreamingSetNavMeshConnection
from .hkaiStreamingSetVolumeConnection import hkaiStreamingSetVolumeConnection
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkaiStreamingSet(hkObject):
    thisUid: UInt32
    oppositeUid: UInt32
    meshConnections: List[hkaiStreamingSetNavMeshConnection]
    graphConnections: List[hkaiStreamingSetGraphConnection]
    volumeConnections: List[hkaiStreamingSetVolumeConnection]

    _meshConnectionsCount_offset: UInt32
    _graphConnectionsCount_offset: UInt32
    _volumeConnectionsCount_offset: UInt32

    def __init__(self):
        super().__init__()

        self.meshConnections = []
        self.graphConnections = []
        self.volumeConnections = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.thisUid = br.read_uint32()
        self.oppositeUid = br.read_uint32()

        meshConnectionsCount_offset = hkFile._assert_pointer(br)
        meshConnectionsCount = hkFile._read_counter(br)

        graphConnectionsCount_offset = hkFile._assert_pointer(br)
        graphConnectionsCount = hkFile._read_counter(br)

        volumeConnectionsCount_offset = hkFile._assert_pointer(br)
        volumeConnectionsCount = hkFile._read_counter(br)

        for lfu in obj.local_fixups:
            br.step_in(lfu.dst)
            if lfu.src == meshConnectionsCount_offset:
                for _ in range(meshConnectionsCount):
                    meshConnection = hkaiStreamingSetNavMeshConnection()
                    meshConnection.deserialize(hkFile, br, obj)
                    self.meshConnections.append(meshConnection)
            elif lfu.src == graphConnectionsCount_offset:
                for _ in range(graphConnectionsCount):
                    graphConnection = hkaiStreamingSetGraphConnection()
                    graphConnection.deserialize(hkFile, br, obj)
                    self.graphConnections.append(graphConnection)
            elif lfu.src == volumeConnectionsCount_offset:
                for _ in range(volumeConnectionsCount):
                    volumeConnection = hkaiStreamingSetVolumeConnection()
                    volumeConnection.deserialize(hkFile, br, obj)
                    self.volumeConnections.append(volumeConnection)
            br.step_out()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_uint32(self.thisUid)
        bw.write_uint32(self.oppositeUid)

        self._meshConnectionsCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, len(self.meshConnections))

        self._graphConnectionsCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, len(self.graphConnections))

        self._volumeConnectionsCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, len(self.volumeConnections))

        # Arrays get written later

    def as_dict(self):
        return {
            "thisUid": self.thisUid,
            "oppositeUid": self.oppositeUid,
            "meshConnections": [mC.as_dict() for mC in self.meshConnections],
            "graphConnections": [gC.as_dict() for gC in self.graphConnections],
            "volumeConnections": [vC.as_dict() for vC in self.volumeConnections],
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()

        inst.thisUid = d["thisUid"]
        inst.oppositeUid = d["oppositeUid"]
        inst.meshConnections = [
            hkaiStreamingSetNavMeshConnection.from_dict(mC)
            for mC in d["meshConnections"]
        ]
        inst.graphConnections = [
            hkaiStreamingSetGraphConnection.from_dict(gC)
            for gC in d["graphConnections"]
        ]
        inst.volumeConnections = [
            hkaiStreamingSetVolumeConnection.from_dict(vC)
            for vC in d["volumeConnections"]
        ]

        return inst
