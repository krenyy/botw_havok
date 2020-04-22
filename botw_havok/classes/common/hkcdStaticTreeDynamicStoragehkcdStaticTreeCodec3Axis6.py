from typing import List

from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32
from ...container.util.localreference import LocalReference
from .hkcdStaticTreeCodec3Axis6 import hkcdStaticTreeCodec3Axis6
from .hkObject import hkObject

if False:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkcdStaticTreeDynamicStoragehkcdStaticTreeCodec3Axis6(hkObject):
    nodes: List[hkcdStaticTreeCodec3Axis6]

    def __init__(self):
        self.nodes = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        nodesCount_offset = br.tell()
        hkFile._assert_pointer(br)
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
        obj.local_references.append(
            LocalReference(hkFile, bw, obj, bw.tell(), self.nodes)
        )
        bw.align_to(16)

    def asdict(self):
        return {"nodes": [node.asdict() for node in self.nodes]}

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()

        inst.nodes = [hkcdStaticTreeCodec3Axis6.fromdict(node) for node in d["nodes"]]

        return inst
