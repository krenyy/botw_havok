from typing import TYPE_CHECKING

import botw_havok.classes.util.class_map as class_map
from .hkpShapeContainer import hkpShapeContainer
from ..base import HKBaseClass
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Int32
from ...container.util.globalreference import GlobalReference

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpSingleShapeContainer(hkpShapeContainer):
    childShape: HKBaseClass

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        for gr in obj.global_references:
            if gr.src_rel_offset == br.tell():
                try:
                    hkFile.data.objects.remove(gr.dst_obj)
                except ValueError:
                    pass

                self.childShape = class_map.HKClassMap.get(gr.dst_obj.hkClass.name)()
                self.childShape.deserialize(
                    hkFile,
                    BinaryReader(
                        initial_bytes=gr.dst_obj.bytes,
                        big_endian=hkFile.header.endian == 0,
                    ),
                    gr.dst_obj,
                )

                hkFile._assert_pointer(br)
                break

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        gr = GlobalReference()
        gr.src_obj = obj
        gr.src_rel_offset = bw.tell()
        gr.dst_section_id = Int32(2)
        obj.global_references.append(gr)

        self.childShape.serialize(
            hkFile, BinaryWriter(big_endian=hkFile.header.endian == 0), gr.dst_obj
        )

        # If an identical HKObject exists,
        # use it instead of creating a new one
        for o in hkFile.data.objects:
            if o.bytes == gr.dst_obj.bytes:
                gr.dst_obj = o
                break
        else:
            hkFile.data.objects.append(gr.dst_obj)

        hkFile._write_empty_pointer(bw)

    def as_dict(self):
        d = hkpShapeContainer.as_dict(self)
        d.update({"childShape": self.childShape})
        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(hkpShapeContainer.from_dict(d).__dict__)
        inst.childShape = class_map.HKClassMap.get(
            d["childShape"]["hkClass"]
        ).from_dict(d["childShape"])

        return inst
