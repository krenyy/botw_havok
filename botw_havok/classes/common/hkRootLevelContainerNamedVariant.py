from typing import List

import botw_havok.classes.util.class_map as class_map

from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Int32, String
from ...container.util.globalreference import GlobalReference
from ...container.util.localfixup import LocalFixup
from ...container.util.localreference import LocalReference
from ..base import HKBaseClass
from .hkObject import hkObject

if False:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkRootLevelContainerNamedVariant(hkObject):
    name: String
    className: String
    variant: HKBaseClass

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        name_offset = br.tell()
        hkFile._assert_pointer(br)  # name

        className_offset = br.tell()
        hkFile._assert_pointer(br)  # className

        variant_offset = br.tell()
        hkFile._assert_pointer(br)  # variant

        for lfu in obj.local_fixups:
            br.step_in(lfu.dst)
            if lfu.src == name_offset:
                self.name = br.read_string()
            elif lfu.src == className_offset:
                self.className = br.read_string()
            br.step_out()

        for gr in obj.global_references:
            if gr.src_rel_offset == variant_offset:
                self.variant = class_map.HKClassMap.get(gr.dst_obj.hkClass.name)()
                self.variant.deserialize(
                    hkFile,
                    BinaryReader(
                        initial_bytes=gr.dst_obj.bytes,
                        big_endian=hkFile.header.endian == 0,
                    ),
                    gr.dst_obj,
                )

                hkFile.data.objects.remove(gr.dst_obj)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        obj.local_references.append(
            LocalReference(hkFile, bw, obj, bw.tell(), self.name)
        )
        hkFile._write_empty_pointer(bw)  # name

        obj.local_references.append(
            LocalReference(hkFile, bw, obj, bw.tell(), self.className)
        )
        hkFile._write_empty_pointer(bw)  # className

        # Add reference to the nested 'variant' object
        gr = GlobalReference()
        gr.src_obj = obj
        gr.src_rel_offset = bw.tell()
        gr.dst_section_id = Int32(2)
        obj.global_references.append(gr)
        hkFile._write_empty_pointer(bw)  # variant

        hkFile.data.objects.append(gr.dst_obj)

        self.variant.serialize(
            hkFile, BinaryWriter(big_endian=hkFile.header.endian == 0), gr.dst_obj
        )

    def asdict(self):
        return {
            "name": self.name,
            "className": self.className,
            "variant": self.variant.asdict(),
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.name = d["name"]
        inst.className = d["className"]
        inst.variant = class_map.HKClassMap.get(d["className"]).fromdict(d["variant"])

        return inst

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.name}, {self.className}, {self.variant})"
        )
