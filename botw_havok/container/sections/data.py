import typing

from ...binary import BinaryReader, BinaryWriter
import botw_havok.classes.util.class_map as util
from .base import HKSection
from .classnames import HKClass
from .util import GlobalFixup, GlobalReference, LocalFixup
from .hkobject import HKObject

if False:
    from ...classes.base import HKBase
    from ...hk import HK


class HKDataSection(HKSection):
    """Havok __data__ section
    """

    id: int = 2
    tag: str = "__data__"

    global_references: typing.List[GlobalReference]

    objects: typing.List[HKObject]
    contents: typing.List["HKBase"]

    def __init__(self):
        super().__init__()
        self.global_references = []
        self.objects = []
        self.contents = []

    def read(self, hk: "HK", br: BinaryReader):
        super().read(br)

        # Map out all the objects contained in the data section
        for i, vfu in enumerate(self.virtual_fixups):
            cls = hk.classnames.get(vfu.dst)

            if len(self.virtual_fixups) > i + 1:
                length = self.virtual_fixups[i + 1].src - vfu.src
            else:
                length = self.local_fixups_offset - vfu.src

            obj = HKObject()

            obj.size = length
            obj.hkclass = cls
            obj.read(hk, br, length)

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
                    if ref not in self.global_references:
                        self.global_references.append(ref)

        self.local_fixups.clear()
        self.global_fixups.clear()
        self.virtual_fixups.clear()

        # Seek to the end of the file to check for additional embedded hk files
        br.seek_absolute(self.absolute_offset + self.EOF_offset)

    def deserialize(self, hk: "HK"):
        for obj in self.objects:
            try:
                hkcls = util.HKClassMap.get(obj.hkclass.name)()
                self.contents.append(hkcls)
            except KeyError:
                raise Exception(f"Class '{obj.hkclass.name}' is not mapped out yet.")

            hkcls.deserialize(hk, obj)
        self.objects.clear()

    def serialize(self, hk: "HK"):
        for hkcls in self.contents:
            self.objects.append(hkcls.hkobj)
            hkcls.serialize(hk)
        self.contents.clear()

    def write(self, hk: "HK", bw: BinaryWriter):
        # Clear out all the fixups beforehand
        self.local_fixups.clear()
        self.global_fixups.clear()
        self.virtual_fixups.clear()

        # Set data section absolute offset
        self.absolute_offset = bw.tell()

        # Serialize the file if it happens to be deserialized
        if self.contents:
            raise Exception("You need to serialize first!")

        for obj in self.objects:
            obj.write(hk, bw)
            bw.reservations.update(
                {
                    k: v + obj.offset + self.absolute_offset
                    for k, v in obj.reservations.items()
                }
            )

            # Create a Virtual fixup
            vfu = GlobalFixup()
            vfu.src = obj.offset
            vfu.dst_section_id = 0  # __classnames__ section id
            vfu.dst = obj.hkclass.offset

            self.virtual_fixups.append(vfu)

        for gr in self.global_references:
            # Create a Global fixup
            gfu = GlobalFixup()
            gfu.src = gr.src_obj.offset + gr.src_rel_offset
            gfu.dst_section_id = 2
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
            if name == "EOF:uint32":
                bw.fill_uint32(
                    name.split(":")[0], self.absolute_offset + self.EOF_offset
                )
            else:
                raise Exception("There shouldn't be any other unresolved reservations!")

    def get(self, value: int):
        for obj in self.objects:
            if obj.offset == value:
                return obj

    def asdict(self):
        return {
            "contents": [content.asdict() for content in self.contents],
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.contents = [
            util.HKClassMap.get(content["hkClass"]).fromdict(content)
            for content in d["contents"]
        ]
        return inst

    def __repr__(self):
        return "<{} [{}]>".format(
            self.__class__.__name__, self.contents if self.contents else self.objects
        )
