from typing import List

from ..binary import BinaryReader, BinaryWriter
from ..container.sections.util import LocalFixup
from .base import HKBase
from .common.hkpBvCompressedMeshShapeTree import hkpBvCompressedMeshShapeTree
from .common.hkpBvTreeShape import hkpBvTreeShape
from .enums.WeldingType import WeldingType

if False:
    from ..hk import HK
    from ..container.sections.hkobject import HKObject


class hkpBvCompressedMeshShape(HKBase, hkpBvTreeShape):
    convexRadius: float
    weldingType: int

    hasPerPrimitiveCollisionFilterInfo: bool
    hasPerPrimitiveUserData: bool

    collisionFilterInfoPalette: List[int]
    userDataPalette: List[int]
    userStringPalette: List[str]

    tree: hkpBvCompressedMeshShapeTree

    def __init__(self):
        HKBase.__init__(self)

        self.collisionFilterInfoPalette = []
        self.userDataPalette = []
        self.userStringPalette = []

    def deserialize(self, hk: "HK", obj: "HKObject"):
        HKBase.deserialize(self, hk, obj)

        br = BinaryReader(self.hkobj.bytes)
        br.big_endian = hk.header.endian == 0

        hkpBvTreeShape.deserialize(self, hk, br, obj)

        if hk.header.padding_option:
            br.align_to(16)

        hk._assert_pointer(br)  # probably

        self.convexRadius = br.read_single()

        self.weldingType = br.read_uint8()
        self.hasPerPrimitiveCollisionFilterInfo = bool(br.read_int8())
        self.hasPerPrimitiveUserData = bool(br.read_int8())
        br.align_to(4)

        collisionFilterInfoPaletteCount_offset = br.tell()
        collisionFilterInfoPaletteCount = hk._read_counter(br)

        userDataPaletteCount_offset = br.tell()
        userDataPaletteCount = hk._read_counter(br)

        userStringPaletteCount_offset = br.tell()
        userStringPaletteCount = hk._read_counter(br)

        for lfu in self.hkobj.local_fixups:
            if lfu.src == collisionFilterInfoPaletteCount_offset:
                br.step_in(lfu.dst)
                for _ in range(collisionFilterInfoPaletteCount):
                    self.collisionFilterInfoPalette.append(br.read_uint32())
                br.step_out()
        br.align_to(16)

        for lfu in self.hkobj.local_fixups:
            if lfu.src == userDataPaletteCount_offset:
                br.step_in(lfu.dst)
                for _ in range(userDataPaletteCount):
                    self.userDataPalette.append(br.read_uint32())
                br.step_out()
        br.align_to(16)

        for lfu in self.hkobj.local_fixups:
            br.step_in(lfu.dst)
            if lfu.src == userStringPaletteCount_offset:
                for _ in range(userStringPaletteCount):
                    hk._assert_pointer(br)
                for _ in range(userStringPaletteCount):
                    self.userStringPalette.append(br.read_string())
                    br.align_to(2)
            br.step_out()
        br.align_to(16)

        self.tree = hkpBvCompressedMeshShapeTree()
        self.tree.deserialize(hk, br, obj)

    def serialize(self, hk: "HK"):
        HKBase.assign_class(self, hk)

        bw = BinaryWriter()
        bw.big_endian = hk.header.endian == 0

        hkpBvTreeShape.serialize(self, hk, bw)

        if hk.header.padding_option:
            bw.align_to(16)

        hk._write_empty_pointer(bw)  # probably

        bw.write_single(self.convexRadius)

        bw.write_uint8(self.weldingType)
        bw.write_uint8(int(self.hasPerPrimitiveCollisionFilterInfo))
        bw.write_uint8(int(self.hasPerPrimitiveUserData))
        bw.align_to(4)

        collisionFilterInfoPaletteCount_offset = bw.tell()
        hk._write_counter(bw, len(self.collisionFilterInfoPalette))

        userDataPaletteCount_offset = bw.tell()
        hk._write_counter(bw, len(self.userDataPalette))

        userStringPaletteCount_offset = bw.tell()
        hk._write_counter(bw, len(self.userStringPalette))
        bw.align_to(16)

        self.tree.serialize(hk, bw)
        bw.align_to(16)

        # Write array data

        collisionFilterInfoPalette_offset = bw.tell()
        for colInfo in self.collisionFilterInfoPalette:
            bw.write_uint32(colInfo)
        bw.align_to(16)

        self.hkobj.local_fixups.append(
            LocalFixup(
                collisionFilterInfoPaletteCount_offset,
                collisionFilterInfoPalette_offset,
            )
        )

        userDataPalette_offset = bw.tell()
        for userData in self.userDataPalette:
            bw.write_uint32(userData)
        bw.align_to(16)

        self.hkobj.local_fixups.append(
            LocalFixup(userDataPaletteCount_offset, userDataPalette_offset)
        )

        # ----

        if self.userStringPalette:
            userStringPalette_offset = bw.tell()
            userString_sources = []  # Messy as heck but I don't care
            userString_destinations = []
            for userString in self.userStringPalette:
                userString_sources.append(bw.tell())
                hk._write_empty_pointer(bw)
            for userString in self.userStringPalette:
                userString_destinations.append(bw.tell())
                bw.write_string(userString)
                bw.align_to(2)  # TODO: Check if correct
            bw.align_to(16)

            self.hkobj.local_fixups.append(
                LocalFixup(userStringPaletteCount_offset, userStringPalette_offset)
            )

            for src, dst in zip(userString_sources, userString_destinations):
                self.hkobj.local_fixups.append(LocalFixup(src, dst))

        # ----

        if self.tree.nodes:
            nodes_offset = bw.tell()
            for node in self.tree.nodes:
                node.serialize(hk, bw, self.hkobj)
            bw.align_to(16)

            self.hkobj.local_fixups.append(
                LocalFixup(self.tree._nodesCount_offset, nodes_offset)
            )

        # ----
        # ----

        if self.tree.sections:
            sections_offset = bw.tell()
            for section in self.tree.sections:
                section.serialize(hk, bw, self.hkobj)
            bw.align_to(16)

            self.hkobj.local_fixups.append(
                LocalFixup(self.tree._sectionsCount_offset, sections_offset)
            )

            for section in self.tree.sections:
                if section.nodes:
                    section_nodes_offset = bw.tell()
                    for node in section.nodes:
                        node.serialize(hk, bw, self.hkobj)
                    self.hkobj.local_fixups.append(
                        LocalFixup(section._nodesCount_offset, section_nodes_offset)
                    )
                    bw.align_to(16)

        # ----

        if self.tree.primitives:
            primitives_offset = bw.tell()
            for primitive in self.tree.primitives:
                primitive.serialize(hk, bw, self.hkobj)
            bw.align_to(16)

            self.hkobj.local_fixups.append(
                LocalFixup(self.tree._primitivesCount_offset, primitives_offset)
            )

        # ----

        if self.tree.sharedVerticesIndex:
            sharedVerticesIndex_offset = bw.tell()
            for sVI in self.tree.sharedVerticesIndex:
                bw.write_uint16(sVI)
            bw.align_to(16)

            self.hkobj.local_fixups.append(
                LocalFixup(
                    self.tree._sharedVerticesIndexCount_offset,
                    sharedVerticesIndex_offset,
                )
            )

        # ----
        # ----

        if self.tree.packedVertices:
            packedVertices_offset = bw.tell()
            for pV in self.tree.packedVertices:
                bw.write_uint32(pV)
            bw.align_to(16)

            self.hkobj.local_fixups.append(
                LocalFixup(self.tree._packedVerticesCount_offset, packedVertices_offset)
            )

        if self.tree.sharedVertices:
            sharedVertices_offset = bw.tell()
            for sV in self.tree.sharedVertices:
                bw.write_uint64(sV)
            bw.align_to(16)

            self.hkobj.local_fixups.append(
                LocalFixup(self.tree._sharedVerticesCount_offset, sharedVertices_offset)
            )

        if self.tree.primitiveDataRuns:
            primitiveDataRuns_offset = bw.tell()
            for dataRun in self.tree.primitiveDataRuns:
                dataRun.serialize(hk, bw)
            bw.align_to(16)

            self.hkobj.local_fixups.append(
                LocalFixup(
                    self.tree._primitiveDataRunsCount_offset, primitiveDataRuns_offset
                )
            )

        HKBase.serialize(self, hk, bw)

    def asdict(self):
        d = HKBase.asdict(self)
        d.update(hkpBvTreeShape.asdict(self))

        d.update(
            {
                "convexRadius": self.convexRadius,
                "weldingType": WeldingType(self.weldingType).name,
                "hasPerPrimitiveCollisionFilterInfo": self.hasPerPrimitiveCollisionFilterInfo,
                "hasPerPrimitiveUserData": self.hasPerPrimitiveUserData,
                "collisionFilterInfoPalette": [
                    hex(i) for i in self.collisionFilterInfoPalette
                ],
                "userDataPalette": [hex(i) for i in self.userDataPalette],
                "userStringPalette": self.userStringPalette,
                "tree": self.tree.asdict(),
            }
        )

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBase.fromdict(d).__dict__)
        inst.__dict__.update(hkpBvTreeShape.fromdict(d).__dict__)

        inst.convexRadius = d["convexRadius"]
        inst.weldingType = WeldingType[d["weldingType"]].value
        inst.hasPerPrimitiveCollisionFilterInfo = d[
            "hasPerPrimitiveCollisionFilterInfo"
        ]
        inst.hasPerPrimitiveUserData = d["hasPerPrimitiveUserData"]
        inst.collisionFilterInfoPalette = [
            int(i, base=16) for i in d["collisionFilterInfoPalette"]
        ]
        inst.userDataPalette = [int(i, base=16) for i in d["userDataPalette"]]
        inst.userStringPalette = d["userStringPalette"]
        inst.tree = hkpBvCompressedMeshShapeTree.fromdict(d["tree"])

        return inst
