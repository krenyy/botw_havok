from typing import List
from .hkcdStaticTreeCodec3Axis5 import hkcdStaticTreeCodec3Axis5
from ...binary import BinaryReader, BinaryWriter

if False:
    from ...hk import HK
    from ...container.sections.hkobject import HKObject


class hkcdStaticTreeDynamicStoragehkcdStaticTreeCodec3Axis5:
    _nodesCount_offset: int
    nodes: List[hkcdStaticTreeCodec3Axis5]

    def __init__(self):
        self.nodes = []

    def deserialize(self, hk: "HK", br: BinaryReader, obj: "HKObject"):
        nodesCount_offset = br.tell()
        nodesCount = hk._read_counter(br)

        br.align_to(16)

        for lfu in obj.local_fixups:
            br.step_in(lfu.dst)

            if lfu.src == nodesCount_offset:
                for _ in range(nodesCount):
                    node = hkcdStaticTreeCodec3Axis5()
                    self.nodes.append(node)
                    node.deserialize(hk, br, obj)

            br.step_out()

    def serialize(self, hk: "HK", bw: BinaryWriter):
        self._nodesCount_offset = bw.tell()
        hk._write_counter(bw, len(self.nodes))

        bw.align_to(16)

        # Individual nodes get written later

    def asdict(self):
        return {"nodes": [node.asdict() for node in self.nodes]}

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()

        inst.nodes = [hkcdStaticTreeCodec3Axis5.fromdict(node) for node in d["nodes"]]

        return inst
