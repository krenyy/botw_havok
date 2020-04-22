from typing import List

from ..binary import BinaryReader, BinaryWriter
from ..binary.types import Bool, Float32, String, UInt8, UInt32
from ..container.util.localfixup import LocalFixup
from ..container.util.localreference import LocalReference
from .base import HKBaseClass
from .common.hkpBvCompressedMeshShapeTree import hkpBvCompressedMeshShapeTree
from .common.hkpBvTreeShape import hkpBvTreeShape
from .enums.WeldingType import WeldingType

if False:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkpBvCompressedMeshShape(HKBaseClass, hkpBvTreeShape):
    convexRadius: Float32
    weldingType: UInt8

    hasPerPrimitiveCollisionFilterInfo: Bool
    hasPerPrimitiveUserData: Bool

    collisionFilterInfoPalette: List[UInt32]
    userDataPalette: List[UInt32]
    userStringPalette: List[String]

    tree: hkpBvCompressedMeshShapeTree

    def __init__(self):
        HKBaseClass.__init__(self)
        hkpBvTreeShape.__init__(self)

        self.collisionFilterInfoPalette = []
        self.userDataPalette = []
        self.userStringPalette = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        HKBaseClass.deserialize(self, hkFile, br, obj)
        hkpBvTreeShape.deserialize(self, hkFile, br, obj)

        ###

        if hkFile.header.padding_option:
            br.align_to(16)

        hkFile._assert_pointer(br)  # probably

        self.convexRadius = br.read_float32()

        self.weldingType = br.read_uint8()
        self.hasPerPrimitiveCollisionFilterInfo = Bool(br.read_int8())
        self.hasPerPrimitiveUserData = Bool(br.read_int8())
        br.align_to(4)

        collisionFilterInfoPaletteCount_offset = br.tell()
        hkFile._assert_pointer(br)
        collisionFilterInfoPaletteCount = hkFile._read_counter(br)

        userDataPaletteCount_offset = br.tell()
        hkFile._assert_pointer(br)
        userDataPaletteCount = hkFile._read_counter(br)

        userStringPaletteCount_offset = br.tell()
        hkFile._assert_pointer(br)
        userStringPaletteCount = hkFile._read_counter(br)

        br.align_to(16)

        for lfu in obj.local_fixups:
            br.step_in(lfu.dst)
            if lfu.src == collisionFilterInfoPaletteCount_offset:
                for _ in range(collisionFilterInfoPaletteCount):
                    self.collisionFilterInfoPalette.append(br.read_uint32())
            elif lfu.src == userDataPaletteCount_offset:
                for _ in range(userDataPaletteCount):
                    self.userDataPalette.append(br.read_uint32())
            elif lfu.src == userStringPaletteCount_offset:
                for _ in range(userStringPaletteCount):
                    hkFile._assert_pointer(br)
                for _ in range(userStringPaletteCount):
                    self.userStringPalette.append(br.read_string())
                    br.align_to(2)
            br.step_out()

        self.tree = hkpBvCompressedMeshShapeTree()
        self.tree.deserialize(hkFile, br, obj)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        HKBaseClass.assign_class(self, hkFile, obj)
        hkpBvTreeShape.serialize(self, hkFile, bw, obj)

        ###

        if hkFile.header.padding_option:
            bw.align_to(16)

        hkFile._write_empty_pointer(bw)  # probably

        bw.write_float32(Float32(self.convexRadius))

        bw.write_uint8(UInt8(self.weldingType))
        bw.write_uint8(UInt8(self.hasPerPrimitiveCollisionFilterInfo))
        bw.write_uint8(UInt8(self.hasPerPrimitiveUserData))
        bw.align_to(4)

        obj.local_references.append(
            LocalReference(hkFile, bw, obj, bw.tell(), self.collisionFilterInfoPalette)
        )
        obj.local_references.append(
            LocalReference(hkFile, bw, obj, bw.tell(), self.userDataPalette)
        )

        obj.local_references.append(
            LocalReference(hkFile, bw, obj, bw.tell(), self.userStringPalette)
        )

        bw.align_to(16)

        self.tree.serialize(hkFile, bw, obj)
        bw.align_to(16)

        ###

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def asdict(self):
        d = HKBaseClass.asdict(self)
        d.update(hkpBvTreeShape.asdict(self))

        d.update(
            {
                "convexRadius": self.convexRadius,
                "weldingType": WeldingType(self.weldingType).name,
                "hasPerPrimitiveCollisionFilterInfo": self.hasPerPrimitiveCollisionFilterInfo,
                "hasPerPrimitiveUserData": self.hasPerPrimitiveUserData,
                "collisionFilterInfoPalette": self.collisionFilterInfoPalette,
                "userDataPalette": self.userDataPalette,
                "userStringPalette": self.userStringPalette,
                "tree": self.tree.asdict(),
            }
        )

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBaseClass.fromdict(d).__dict__)
        inst.__dict__.update(hkpBvTreeShape.fromdict(d).__dict__)

        inst.convexRadius = d["convexRadius"]
        inst.weldingType = WeldingType[d["weldingType"]].value
        inst.hasPerPrimitiveCollisionFilterInfo = d[
            "hasPerPrimitiveCollisionFilterInfo"
        ]
        inst.hasPerPrimitiveUserData = d["hasPerPrimitiveUserData"]
        inst.collisionFilterInfoPalette = d["collisionFilterInfoPalette"]
        inst.userDataPalette = d["userDataPalette"]
        inst.userStringPalette = d["userStringPalette"]
        inst.tree = hkpBvCompressedMeshShapeTree.fromdict(d["tree"])

        return inst
