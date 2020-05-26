from typing import List
from typing import TYPE_CHECKING

from .hkObject import hkObject
from .hkcdStaticTreeCodec3Axis5 import hkcdStaticTreeCodec3Axis5
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkcdStaticTreeDynamicStoragehkcdStaticTreeCodec3Axis5(hkObject):
    nodes: List[hkcdStaticTreeCodec3Axis5]

    # TODO: Get rid of these things sometime
    _nodesCount_offset: UInt32

    def __init__(self):
        self.nodes = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        nodesCount_offset = hkFile._assert_pointer(br)
        nodesCount = hkFile._read_counter(br)

        br.align_to(16)

        for lfu in obj.local_fixups:
            br.step_in(lfu.dst)

            if lfu.src == nodesCount_offset:
                for _ in range(nodesCount):
                    node = hkcdStaticTreeCodec3Axis5()
                    self.nodes.append(node)
                    node.deserialize(hkFile, br, obj)

            br.step_out()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        self._nodesCount_offset = bw.tell()

        hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.nodes)))

        bw.align_to(16)

        # The nodes get written at a later stage

    def as_dict(self):
        return {"nodes": [node.as_dict() for node in self.nodes]}

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()

        inst.nodes = [hkcdStaticTreeCodec3Axis5.from_dict(node) for node in d["nodes"]]

        return inst
