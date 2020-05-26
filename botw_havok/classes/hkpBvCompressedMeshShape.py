from typing import List
from typing import TYPE_CHECKING

from .base import HKBaseClass
from .common.hkpBvCompressedMeshShapeTree import hkpBvCompressedMeshShapeTree
from .common.hkpBvTreeShape import hkpBvTreeShape
from .enums.WeldingType import WeldingType
from ..binary import BinaryReader, BinaryWriter
from ..binary.types import Float32, UInt8, UInt32
from ..container.util.localfixup import LocalFixup

if TYPE_CHECKING:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkpBvCompressedMeshShape(HKBaseClass, hkpBvTreeShape):
    convexRadius: Float32
    weldingType: UInt8

    hasPerPrimitiveCollisionFilterInfo: bool
    hasPerPrimitiveUserData: bool

    collisionFilterInfoPalette: List[UInt32]
    userDataPalette: List[UInt32]
    userStringPalette: List[str]

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
        self.hasPerPrimitiveCollisionFilterInfo = bool(br.read_int8())
        self.hasPerPrimitiveUserData = bool(br.read_int8())
        br.align_to(4)

        collisionFilterInfoPaletteCount_offset = hkFile._assert_pointer(br)
        collisionFilterInfoPaletteCount = hkFile._read_counter(br)

        userDataPaletteCount_offset = hkFile._assert_pointer(br)
        userDataPaletteCount = hkFile._read_counter(br)

        userStringPaletteCount_offset = hkFile._assert_pointer(br)
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

        collisionFilterInfoPaletteCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.collisionFilterInfoPalette)))

        userDataPaletteCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.userDataPalette)))

        userStringPaletteCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.userStringPalette)))

        bw.align_to(16)

        self.tree.serialize(hkFile, bw, obj)
        bw.align_to(16)

        ####################
        # Write array data #
        ####################

        # collisionFilterInfoPalette

        obj.local_fixups.append(
            LocalFixup(collisionFilterInfoPaletteCount_offset, bw.tell())
        )
        [
            bw.write_uint32(collisionFilterInfo)
            for collisionFilterInfo in self.collisionFilterInfoPalette
        ]
        bw.align_to(16)

        # userDataPalette

        obj.local_fixups.append(LocalFixup(userDataPaletteCount_offset, bw.tell()))
        [bw.write_uint32(userData) for userData in self.userDataPalette]
        bw.align_to(16)

        # userStringPalette

        if self.userStringPalette:
            obj.local_fixups.append(
                LocalFixup(userStringPaletteCount_offset, bw.tell())
            )

            userString_sources = []  # Messy as heck but I don't care
            userString_destinations = []

            for _ in enumerate(self.userStringPalette):
                userString_sources.append(bw.tell())
                hkFile._write_empty_pointer(bw)

            for userString in self.userStringPalette:
                userString_destinations.append(bw.tell())
                bw.write_string(userString)
                bw.align_to(2)
            bw.align_to(16)

            for src, dst in zip(userString_sources, userString_destinations):
                obj.local_fixups.append(LocalFixup(src, dst))

        # --------------------------------
        # hkpBvCompressedMeshShapeTree
        # nodes

        if self.tree.nodes:
            obj.local_fixups.append(LocalFixup(self.tree._nodesCount_offset, bw.tell()))

            [node.serialize(hkFile, bw, obj) for node in self.tree.nodes]
            bw.align_to(16)

        # sections
        if self.tree.sections:
            obj.local_fixups.append(
                LocalFixup(self.tree._sectionsCount_offset, bw.tell())
            )

            [section.serialize(hkFile, bw, obj) for section in self.tree.sections]
            bw.align_to(16)

            for section in self.tree.sections:
                if section.nodes:
                    obj.local_fixups.append(
                        LocalFixup(section._nodesCount_offset, bw.tell())
                    )

                    [node.serialize(hkFile, bw, obj) for node in section.nodes]
                    bw.align_to(16)

        # primitives
        if self.tree.primitives:
            obj.local_fixups.append(
                LocalFixup(self.tree._primitivesCount_offset, bw.tell())
            )

            [primitive.serialize(hkFile, bw, obj) for primitive in self.tree.primitives]
            bw.align_to(16)

        # sharedVerticesIndex
        if self.tree.sharedVerticesIndex:
            obj.local_fixups.append(
                LocalFixup(self.tree._sharedVerticesIndexCount_offset, bw.tell())
            )

            [bw.write_uint16(sVI) for sVI in self.tree.sharedVerticesIndex]
            bw.align_to(16)

        # packedVertices
        if self.tree.packedVertices:
            obj.local_fixups.append(
                LocalFixup(self.tree._packedVerticesCount_offset, bw.tell())
            )

            [bw.write_uint32(packedVertex) for packedVertex in self.tree.packedVertices]

            bw.align_to(16)

        # sharedVertices
        if self.tree.sharedVertices:
            obj.local_fixups.append(
                LocalFixup(self.tree._sharedVerticesCount_offset, bw.tell())
            )

            [bw.write_uint64(sharedVertex) for sharedVertex in self.tree.sharedVertices]

            bw.align_to(16)

        # primitiveDataRuns
        if self.tree.primitiveDataRuns:
            obj.local_fixups.append(
                LocalFixup(self.tree._primitiveDataRunsCount_offset, bw.tell())
            )

            [
                primitiveDataRun.serialize(hkFile, bw, obj)
                for primitiveDataRun in self.tree.primitiveDataRuns
            ]

            bw.align_to(16)

        ###

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def as_dict(self):
        d = HKBaseClass.as_dict(self)
        d.update(hkpBvTreeShape.as_dict(self))

        d.update(
            {
                "convexRadius": self.convexRadius,
                "weldingType": WeldingType(self.weldingType).name,
                "hasPerPrimitiveCollisionFilterInfo": bool(
                    self.hasPerPrimitiveCollisionFilterInfo
                ),
                "hasPerPrimitiveUserData": bool(self.hasPerPrimitiveUserData),
                "collisionFilterInfoPalette": self.collisionFilterInfoPalette,
                "userDataPalette": self.userDataPalette,
                "userStringPalette": self.userStringPalette,
                "tree": self.tree.as_dict(),
            }
        )

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBaseClass.from_dict(d).__dict__)
        inst.__dict__.update(hkpBvTreeShape.from_dict(d).__dict__)

        inst.convexRadius = d["convexRadius"]
        inst.weldingType = WeldingType[d["weldingType"]].value
        inst.hasPerPrimitiveCollisionFilterInfo = d[
            "hasPerPrimitiveCollisionFilterInfo"
        ]

        inst.hasPerPrimitiveUserData = d["hasPerPrimitiveUserData"]
        inst.collisionFilterInfoPalette = d["collisionFilterInfoPalette"]
        inst.userDataPalette = d["userDataPalette"]
        inst.userStringPalette = d["userStringPalette"]
        inst.tree = hkpBvCompressedMeshShapeTree.from_dict(d["tree"])

        return inst
