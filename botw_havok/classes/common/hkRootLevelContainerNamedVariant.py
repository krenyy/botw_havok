from typing import TYPE_CHECKING

import botw_havok.classes.util.class_map as class_map
from .hkObject import hkObject
from ..base import HKBaseClass
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkRootLevelContainerNamedVariant(hkObject):
    name: str
    className: str
    variant: HKBaseClass

    _namePointer_offset: UInt32
    _classNamePointer_offset: UInt32
    _variantPointer_offset: UInt32

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        name_offset = hkFile._assert_pointer(br)  # name

        className_offset = hkFile._assert_pointer(br)  # className

        variant_offset = hkFile._assert_pointer(br)  # variant

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
        self._namePointer_offset = hkFile._write_empty_pointer(bw)
        self._classNamePointer_offset = hkFile._write_empty_pointer(bw)
        self._variantPointer_offset = hkFile._write_empty_pointer(bw)

    def as_dict(self):
        return {
            "name": self.name,
            "className": self.className,
            "variant": self.variant.as_dict(),
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.name = d["name"]
        inst.className = d["className"]
        inst.variant = class_map.HKClassMap.get(d["className"]).from_dict(d["variant"])

        return inst

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.name}, {self.className}, {self.variant})"
        )
