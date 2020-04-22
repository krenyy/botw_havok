from typing import List

from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32
from ...container.util.localreference import LocalReference
from .hkcdStaticTreeCodec3Axis5 import hkcdStaticTreeCodec3Axis5
from .hkObject import hkObject

if False:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkcdStaticTreeDynamicStoragehkcdStaticTreeCodec3Axis5(hkObject):
    nodes: List[hkcdStaticTreeCodec3Axis5]

    def __init__(self):
        self.nodes = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        nodesCount_offset = br.tell()
        hkFile._assert_pointer(br)
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
        obj.local_references.append(
            LocalReference(hkFile, bw, obj, bw.tell(), self.nodes)
        )
        bw.align_to(16)

    def asdict(self):
        return {"nodes": [node.asdict() for node in self.nodes]}

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()

        inst.nodes = [hkcdStaticTreeCodec3Axis5.fromdict(node) for node in d["nodes"]]

        return inst
