from typing import List
from typing import TYPE_CHECKING

from .hkObject import hkObject
from .hkcdStaticTreeCodec3Axis6 import hkcdStaticTreeCodec3Axis6
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkcdStaticTreeDynamicStoragehkcdStaticTreeCodec3Axis6(hkObject):
    nodes: List[hkcdStaticTreeCodec3Axis6]

    _nodesCount_offset: UInt32

    def __init__(self):
        self.nodes = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        nodesCount_offset = hkFile._assert_pointer(br)
        nodesCount = hkFile._read_counter(br)

        br.align_to(16)

        for lfu in obj.local_fixups:
            if lfu.src == nodesCount_offset:
                br.step_in(lfu.dst)

                for _ in range(nodesCount):
                    node = hkcdStaticTreeCodec3Axis6()
                    node.deserialize(hkFile, br, obj)

                    self.nodes.append(node)

                br.step_out()

                break

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        self._nodesCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.nodes)))

        bw.align_to(16)

        # Nodes get written later

    def as_dict(self):
        return {"nodes": [node.as_dict() for node in self.nodes]}

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()

        inst.nodes = [hkcdStaticTreeCodec3Axis6.from_dict(node) for node in d["nodes"]]

        return inst
