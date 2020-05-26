from typing import List
from typing import TYPE_CHECKING

from .base import HKBaseClass
from .common.hkcdStaticTreeDefaultTreeStorage6 import hkcdStaticTreeDefaultTreeStorage6
from .common.hkpBvTreeShape import hkpBvTreeShape
from .common.hkpShapeKeyTable import hkpShapeKeyTable
from .common.hkpStaticCompoundShapeInstance import hkpStaticCompoundShapeInstance
from ..binary import BinaryReader, BinaryWriter
from ..binary.types import Int8, UInt16, UInt32
from ..container.util.localfixup import LocalFixup

if TYPE_CHECKING:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkpStaticCompoundShape(HKBaseClass, hkpBvTreeShape):
    numBitsForChildShapeKey: Int8
    referencePolicy: Int8
    childShapeKeyMask: UInt32

    instances: List[hkpStaticCompoundShapeInstance]
    instanceExtraInfos: List[UInt16]

    disabledLargeShapeKeyTable: hkpShapeKeyTable
    tree: hkcdStaticTreeDefaultTreeStorage6

    def __init__(self):
        super().__init__()

        self.instances = []
        self.instanceExtraInfos = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        HKBaseClass.deserialize(self, hkFile, br, obj)
        hkpBvTreeShape.deserialize(self, hkFile, br, obj)

        ###

        if hkFile.header.padding_option:
            br.align_to(16)

        hkFile._assert_pointer(br)

        self.numBitsForChildShapeKey = br.read_int8()
        self.referencePolicy = br.read_int8()
        br.align_to(4)

        self.childShapeKeyMask = br.read_uint32()

        instancesCount_offset = hkFile._assert_pointer(br)
        instancesCount = hkFile._read_counter(br)

        instanceExtraInfosCount_offset = hkFile._assert_pointer(br)
        instanceExtraInfosCount = hkFile._read_counter(br)

        for lfu in obj.local_fixups:
            if lfu.src == instancesCount_offset:
                br.step_in(lfu.dst)

                for _ in range(instancesCount):
                    inst = hkpStaticCompoundShapeInstance()
                    self.instances.append(inst)
                    inst.deserialize(hkFile, br, obj)

                br.step_out()

            if lfu.src == instanceExtraInfosCount_offset:
                br.step_in(lfu.dst)

                for _ in range(instanceExtraInfosCount):
                    self.instanceExtraInfos.append(br.read_uint16())

                br.step_out()

        self.disabledLargeShapeKeyTable = hkpShapeKeyTable()
        self.disabledLargeShapeKeyTable.deserialize(hkFile, br, obj)

        self.tree = hkcdStaticTreeDefaultTreeStorage6()
        self.tree.deserialize(hkFile, br, obj)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        HKBaseClass.assign_class(self, hkFile, obj)
        hkpBvTreeShape.serialize(self, hkFile, bw, obj)

        ###

        if hkFile.header.padding_option:
            bw.align_to(16)

        hkFile._write_empty_pointer(bw)

        bw.write_int8(self.numBitsForChildShapeKey)
        bw.write_int8(self.referencePolicy)
        bw.align_to(4)

        bw.write_uint32(self.childShapeKeyMask)

        instancesCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.instances)))

        instanceExtraInfosCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.instanceExtraInfos)))

        self.disabledLargeShapeKeyTable.serialize(hkFile, bw, obj)
        self.tree.serialize(hkFile, bw, obj)

        ####################
        # Write array data #
        ####################

        if self.instances:
            obj.local_fixups.append(LocalFixup(instancesCount_offset, bw.tell()))

            [instance.serialize(hkFile, bw, obj) for instance in self.instances]

        if self.instanceExtraInfos:
            obj.local_fixups.append(
                LocalFixup(instanceExtraInfosCount_offset, bw.tell())
            )

            [
                bw.write_uint16(instanceExtraInfo)
                for instanceExtraInfo in self.instanceExtraInfos
            ]

        if self.tree.nodes:
            obj.local_fixups.append(LocalFixup(self.tree._nodesCount_offset, bw.tell()))

            [node.serialize(hkFile, bw, obj) for node in self.tree.nodes]

        ###

        bw.align_to(16)

        ###

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def as_dict(self):
        d = HKBaseClass.as_dict(self)
        d.update(hkpBvTreeShape.as_dict(self))
        d.update(
            {
                "numBitsForChildShapeKey": self.numBitsForChildShapeKey,
                "referencePolicy": self.referencePolicy,
                "childShapeKeyMask": self.childShapeKeyMask,
                "instances": [inst.as_dict() for inst in self.instances],
                "instanceExtraInfos": self.instanceExtraInfos,
                "disabledLargeShapeKeyTable": self.disabledLargeShapeKeyTable.as_dict(),
                "tree": self.tree.as_dict(),
            }
        )

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().from_dict(d).__dict__)
        inst.__dict__.update(hkpBvTreeShape.from_dict(d).__dict__)

        inst.numBitsForChildShapeKey = d["numBitsForChildShapeKey"]
        inst.referencePolicy = d["referencePolicy"]
        inst.childShapeKeyMask = d["childShapeKeyMask"]
        inst.instances = [
            hkpStaticCompoundShapeInstance.from_dict(inst) for inst in d["instances"]
        ]
        inst.instanceExtraInfos = d["instanceExtraInfos"]
        inst.disabledLargeShapeKeyTable = hkpShapeKeyTable.from_dict(
            d["disabledLargeShapeKeyTable"]
        )
        inst.tree = hkcdStaticTreeDefaultTreeStorage6.from_dict(d["tree"])

        return inst
