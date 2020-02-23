from typing import List

import botw_havok.classes.util.class_map as util

from ...binary import BinaryReader, BinaryWriter
from ...container.sections.util import GlobalReference, LocalFixup
from .hkReferencedObject import hkReferencedObject

if False:
    from ...hk import HK
    from ...container.sections.hkobject import HKObject


class hkRootLevelContainerNamedVariant:
    name: str
    className: str
    variant: hkReferencedObject

    def deserialize(self, hk: "HK", br: BinaryReader, obj: "HKObject"):
        # name_offset = br.tell()
        hk._assert_pointer(br)  # name

        # className_offset = br.tell()
        hk._assert_pointer(br)  # className

        variant_offset = br.tell()
        hk._assert_pointer(br)  # variant

        self.name = br.read_string()
        br.align_to(16)

        self.className = br.read_string()
        br.align_to(16)

        for gr in obj.global_references:
            if gr.src_rel_offset == variant_offset:
                self.variant = util.HKClassMap.get(gr.dst_obj.hkclass.name)()
                self.variant.deserialize(hk, gr.dst_obj)
                hk.data.objects.remove(gr.dst_obj)

        obj.global_references.clear()

    def serialize(self, hk: "HK", obj: "HKObject", bw: BinaryWriter):
        namePointer_offset = bw.tell()
        hk._write_empty_pointer(bw)  # name

        classNamePointer_offset = bw.tell()
        hk._write_empty_pointer(bw)  # className

        variantPointer_offset = bw.tell()
        hk._write_empty_pointer(bw)  # variant

        name_offset = bw.tell()
        bw.write_string(self.name)
        bw.align_to(16)

        className_offset = bw.tell()
        bw.write_string(self.className)
        bw.align_to(16)

        hk.data.objects.append(self.variant.hkobj)
        self.variant.serialize(hk)

        # Local fixups
        obj.local_fixups.append(LocalFixup(namePointer_offset, name_offset))
        obj.local_fixups.append(LocalFixup(classNamePointer_offset, className_offset))

        # Write reference to the nested object
        gr = GlobalReference()
        gr.src_obj = obj
        gr.src_rel_offset = variantPointer_offset
        gr.dst_obj = self.variant.hkobj
        gr.dst_rel_offset = 0  # i guess?

        obj.global_references.append(gr)

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
        inst.variant = util.HKClassMap.get(d["className"]).fromdict(d["variant"])

        return inst

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.name}, {self.className}, {self.variant})"
        )
