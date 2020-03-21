from typing import List

from ...binary import BinaryReader, BinaryWriter
from .hkcdStaticTreeCodec3Axis6 import hkcdStaticTreeCodec3Axis6

if False:
    from ...hk import HK
    from ...container.sections.hkobject import HKObject


class hkcdStaticTreeDynamicStoragehkcdStaticTreeCodec3Axis6:
    _nodesCount_offset: int
    nodes: List[hkcdStaticTreeCodec3Axis6]

    def __init__(self):
        self.nodes = []

    def deserialize(self, hk: "HK", br: BinaryReader, obj: "HKObject"):
        nodesCount_offset = br.tell()
        nodesCount = hk._read_counter(br)
        br.align_to(16)

        for lfu in obj.local_fixups:
            if lfu.src == nodesCount_offset:
                br.step_in(lfu.dst)

                for _ in range(nodesCount):
                    node = hkcdStaticTreeCodec3Axis6()
                    node.deserialize(hk, br, obj)

                    self.nodes.append(node)

                br.step_out()

                break

    def serialize(self, hk: "HK", bw: BinaryWriter, obj):
        self._nodesCount_offset = bw.tell()
        hk._write_counter(bw, len(self.nodes))
        bw.align_to(16)

        # Nodes get written later

    def asdict(self):
        return {"nodes": [node.asdict() for node in self.nodes]}

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()

        inst.nodes = [hkcdStaticTreeCodec3Axis6.fromdict(node) for node in d["nodes"]]

        return inst
