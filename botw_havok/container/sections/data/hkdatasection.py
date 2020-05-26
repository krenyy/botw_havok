from typing import List, Union
from typing import TYPE_CHECKING

import botw_havok.classes.util.class_map as class_map
from ..base import HKSection
from ...util.globalfixup import GlobalFixup
from ...util.globalreference import GlobalReference
from ...util.hkobject import HKObject
from ...util.virtualfixup import VirtualFixup
from ....binary import BinaryReader, BinaryWriter
from ....binary.types import Int32

if TYPE_CHECKING:
    from ....hkfile import HKFile
    from ....classes.StaticCompoundInfo import StaticCompoundInfo
    from ....classes.hkRootLevelContainer import hkRootLevelContainer
    from ....classes.hkcdStaticAabbTree import hkcdStaticAabbTree
    from ....classes.hkcdStaticTreeDefaultTreeStorage6 import (
        hkcdStaticTreeDefaultTreeStorage6,
    )


class HKDataSection(HKSection):
    """Havok __data__ section
    """

    id: int = 2
    tag: str = "__data__"

    global_references: List[GlobalReference]

    objects: List[HKObject]
    contents: List[
        Union[
            "StaticCompoundInfo",
            "hkRootLevelContainer",
            "hkcdStaticAabbTree",
            "hkcdStaticTreeDefaultTreeStorage6",
        ]
    ]

    def __init__(self):
        super().__init__()
        self.global_references = []
        self.objects = []
        self.contents = []

    def read(self, hkFile: "HKFile", br: BinaryReader):
        super().read(hkFile, br)

        # Map out all the objects contained in the data section
        for i, vfu in enumerate(self.virtual_fixups):
            cls = hkFile.classnames.get(vfu.dst)

            if len(self.virtual_fixups) > i + 1:
                length = self.virtual_fixups[i + 1].src - vfu.src
            else:
                length = self.local_fixups_offset - vfu.src

            obj = HKObject()

            obj.size = length
            obj.hkClass = cls
            obj.read(hkFile, br, length)

            self.objects.append(obj)

        for obj in self.objects:
            # Assign local fixups to respective HK chunks
            for lfu in self.local_fixups:
                if (obj.offset <= lfu.src < obj.offset + obj.size) and (
                        obj.offset <= lfu.dst < obj.offset + obj.size
                ):
                    obj.local_fixups.append(lfu - obj.offset)

            # Assign global references to respective HK chunks
            for gfu in self.global_fixups:
                if obj.offset <= gfu.src < obj.offset + obj.size:
                    ref = GlobalReference()
                    ref.src_obj = obj
                    ref.src_rel_offset = gfu.src - obj.offset
                    ref.dst_obj = self.get(gfu.dst)
                    ref.dst_rel_offset = gfu.dst - ref.dst_obj.offset
                    obj.global_references.append(ref)

        self.local_fixups.clear()
        self.global_fixups.clear()
        self.virtual_fixups.clear()

        # Seek to the end of the file to check for additional embedded hk files
        br.seek_absolute(self.absolute_offset + self.EOF_offset)

    def deserialize(self, hkFile: "HKFile"):
        for obj in self.objects:
            hkcls = class_map.HKClassMap.get(obj.hkClass.name)()
            self.contents.append(hkcls)
            hkcls.deserialize(
                hkFile,
                BinaryReader(
                    initial_bytes=obj.bytes, big_endian=hkFile.header.endian == 0
                ),
                obj,
            )

        self.objects.clear()

    def serialize(self, hkFile: "HKFile"):
        for hkcls in self.contents:
            obj = HKObject()
            self.objects.append(obj)

            hkcls.serialize(
                hkFile, BinaryWriter(big_endian=hkFile.header.endian == 0), obj,
            )
        self.contents.clear()

    def write(self, hkFile: "HKFile", bw: BinaryWriter):
        # Raise exception if deserialized
        if self.contents:
            raise Exception("You need to serialize first!")

        # Clear out all the fixups beforehand
        self.local_fixups.clear()
        self.global_fixups.clear()
        self.virtual_fixups.clear()

        # Set data section absolute offset
        self.absolute_offset = bw.tell()

        for obj in self.objects:
            obj.write(hkFile, bw)
            bw.reservations.update(
                {
                    k: v + obj.offset + self.absolute_offset
                    for k, v in obj.reservations.items()
                }
            )

            # Create a Virtual fixup
            vfu = VirtualFixup()
            vfu.src = obj.offset
            vfu.dst_section_id = Int32(0)  # __classnames__ section id
            vfu.dst = obj.hkClass.offset

            self.virtual_fixups.append(vfu)

        for gr in self.global_references:
            # Create a Global fixup
            gfu = GlobalFixup()
            gfu.src = gr.src_obj.offset + gr.src_rel_offset
            gfu.dst_section_id = Int32(2)
            gfu.dst = gr.dst_obj.offset + gr.dst_rel_offset

            self.global_fixups.append(gfu)

        # Sort fixups by source offset
        # pylama:ignore=E731
        key = lambda x: x.src
        self.local_fixups.sort(key=key)
        self.global_fixups.sort(key=key)
        self.virtual_fixups.sort(key=key)

        # Write local fixups
        self.local_fixups_offset = bw.tell() - self.absolute_offset
        for lfu in self.local_fixups:
            lfu.write(bw)
        bw.align_to(16, b"\xFF")

        # Write global fixups
        self.global_fixups_offset = bw.tell() - self.absolute_offset
        for gfu in self.global_fixups:
            gfu.write(bw)
        bw.align_to(16, b"\xFF")

        # Write virtual fixups
        self.virtual_fixups_offset = bw.tell() - self.absolute_offset
        for vfu in self.virtual_fixups:
            vfu.write(bw)
        bw.align_to(16, b"\xFF")

        self.exports_offset = bw.tell() - self.absolute_offset
        self.imports_offset = bw.tell() - self.absolute_offset
        self.EOF_offset = bw.tell() - self.absolute_offset

        # Fill the reserved header bytes with correct offsets
        bw.fill_uint32(f"{self.tag}abs", self.absolute_offset)
        bw.fill_uint32(f"{self.tag}loc", self.local_fixups_offset)
        bw.fill_uint32(f"{self.tag}glob", self.global_fixups_offset)
        bw.fill_uint32(f"{self.tag}virt", self.virtual_fixups_offset)
        bw.fill_uint32(f"{self.tag}exp", self.exports_offset)
        bw.fill_uint32(f"{self.tag}imp", self.imports_offset)
        bw.fill_uint32(f"{self.tag}eof", self.EOF_offset)

        # This is for StaticCompound files
        # They usually have a StaticCompoundInfo in the first hkfile
        # and other classes in the second one. There's an offset in there
        # that points to the beginning of the second hkfile
        for name in list(bw.reservations):
            if name == "EOF:u32":
                bw.fill_uint32(
                    name.split(":")[0], self.absolute_offset + self.EOF_offset
                )
            else:
                raise Exception("There shouldn't be any other unresolved reservations!")

    def get(self, value: int) -> HKObject:
        for obj in self.objects:
            if obj.offset == value:
                return obj
        else:
            return HKObject()

    def as_dict(self):
        return {
            "contents": [content.as_dict() for content in self.contents],
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.contents = [
            class_map.HKClassMap.get(content["hkClass"]).from_dict(content)
            for content in d["contents"]
        ]
        return inst

    def __repr__(self):
        return "<{} [{}]>".format(
            self.__class__.__name__, self.contents if self.contents else self.objects
        )
