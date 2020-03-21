from typing import List

from ..binary import BinaryReader, BinaryWriter
from ..container.sections.util import LocalFixup
from .base import HKBase
from .common.hkcdStaticTreeDefaultTreeStorage6 import hkcdStaticTreeDefaultTreeStorage6
from .common.hkpBvTreeShape import hkpBvTreeShape
from .common.hkpShapeKeyTable import hkpShapeKeyTable
from .common.hkpStaticCompoundShapeInstance import hkpStaticCompoundShapeInstance

if False:
    from ..hk import HK
    from ..container.sections.hkobject import HKObject


class hkpStaticCompoundShape(HKBase, hkpBvTreeShape):
    numBitsForChildShapeKey: int
    referencePolicy: int
    childShapeKeyMask: int

    instances: List[hkpStaticCompoundShapeInstance]
    instanceExtraInfos: List[int]

    disabledLargeShapeKeyTable: hkpShapeKeyTable
    tree: hkcdStaticTreeDefaultTreeStorage6

    def __init__(self):
        super().__init__()

        self.instances = []
        self.instanceExtraInfos = []

    def deserialize(self, hk: "HK", obj: "HKObject"):
        HKBase.deserialize(self, hk, obj)

        br = BinaryReader(obj.bytes)
        br.big_endian = hk.header.endian == 0

        hkpBvTreeShape.deserialize(self, hk, br, obj)

        if hk.header.padding_option:
            br.align_to(16)

        hk._assert_pointer(br)  # Not sure

        self.numBitsForChildShapeKey = br.read_int8()
        self.referencePolicy = br.read_int8()
        br.align_to(4)

        self.childShapeKeyMask = br.read_uint32()

        instancesCount_offset = br.tell()
        instancesCount = hk._read_counter(br)

        instanceExtraInfosCount_offset = br.tell()
        instanceExtraInfosCount = hk._read_counter(br)

        for lfu in obj.local_fixups:
            if lfu.src == instancesCount_offset:
                br.step_in(lfu.dst)

                for _ in range(instancesCount):
                    inst = hkpStaticCompoundShapeInstance()
                    self.instances.append(inst)
                    inst.deserialize(hk, br, obj)

                br.step_out()

            if lfu.src == instanceExtraInfosCount_offset:
                br.step_in(lfu.dst)

                for _ in range(instanceExtraInfosCount):
                    self.instanceExtraInfos.append(br.read_uint16())

                br.step_out()

        self.disabledLargeShapeKeyTable = hkpShapeKeyTable()
        self.disabledLargeShapeKeyTable.deserialize(hk, br)

        self.tree = hkcdStaticTreeDefaultTreeStorage6()
        self.tree.deserialize(hk, br, obj)

    def serialize(self, hk: "HK"):
        HKBase.assign_class(self, hk)

        bw = BinaryWriter()
        bw.big_endian = hk.header.endian == 0

        hkpBvTreeShape.serialize(self, hk, bw)

        if hk.header.padding_option:
            bw.align_to(16)

        hk._write_empty_pointer(bw)

        bw.write_int8(self.numBitsForChildShapeKey)
        bw.write_int8(self.referencePolicy)
        bw.align_to(4)

        bw.write_uint32(self.childShapeKeyMask)

        instancesCount_offset = bw.tell()
        hk._write_counter(bw, len(self.instances))

        instanceExtraInfosCount_offset = bw.tell()
        hk._write_counter(bw, len(self.instanceExtraInfos))

        self.disabledLargeShapeKeyTable.serialize(hk, bw)
        self.tree.serialize(hk, bw, self.hkobj)

        if self.instances:
            instances_offset = bw.tell()
            for inst in self.instances:
                inst.serialize(hk, bw, self.hkobj)

            self.hkobj.local_fixups.append(
                LocalFixup(instancesCount_offset, instances_offset)
            )

        if self.instanceExtraInfos:
            instanceExtraInfos_offset = bw.tell()
            for instExtraInfo in self.instanceExtraInfos:
                bw.write_uint16(instExtraInfo)

            self.hkobj.local_fixups.append(
                LocalFixup(instanceExtraInfosCount_offset, instanceExtraInfos_offset)
            )

        if self.tree.nodes:
            nodes_offset = bw.tell()
            for node in self.tree.nodes:
                node.serialize(hk, bw, self.hkobj)

            self.hkobj.local_fixups.append(
                LocalFixup(self.tree._nodesCount_offset, nodes_offset)
            )

        bw.align_to(16)

        HKBase.serialize(self, hk, bw)

    def asdict(self):
        d = HKBase.asdict(self)
        d.update(hkpBvTreeShape.asdict(self))
        d.update(
            {
                "numBitsForChildShapeKey": self.numBitsForChildShapeKey,
                "referencePolicy": self.referencePolicy,
                "childShapeKeyMask": self.childShapeKeyMask,
                "instances": [inst.asdict() for inst in self.instances],
                "instanceExtraInfos": self.instanceExtraInfos,
                "disabledLargeShapeKeyTable": self.disabledLargeShapeKeyTable.asdict(),
                "tree": self.tree.asdict(),
            }
        )

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)
        inst.__dict__.update(hkpBvTreeShape.fromdict(d).__dict__)

        inst.numBitsForChildShapeKey = d["numBitsForChildShapeKey"]
        inst.referencePolicy = d["referencePolicy"]
        inst.childShapeKeyMask = d["childShapeKeyMask"]
        inst.instances = [
            hkpStaticCompoundShapeInstance.fromdict(inst) for inst in d["instances"]
        ]
        inst.instanceExtraInfos = d["instanceExtraInfos"]
        inst.disabledLargeShapeKeyTable = hkpShapeKeyTable.fromdict(
            d["disabledLargeShapeKeyTable"]
        )
        inst.tree = hkcdStaticTreeDefaultTreeStorage6.fromdict(d["tree"])

        return inst
