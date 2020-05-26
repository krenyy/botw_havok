from typing import TYPE_CHECKING

import botw_havok.classes.util.class_map as class_map
from .hkObject import hkObject
from ..base import HKBaseClass
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32
from ...container.util.globalreference import GlobalReference

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpCdBody(hkObject):
    shape: HKBaseClass
    shapeKey: UInt32

    # motion: None = None
    # parent: "hkpCdBody" = None

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        for gr in obj.global_references:
            if gr.src_rel_offset == br.tell():
                hkFile.data.objects.remove(gr.dst_obj)
                self.shape = class_map.HKClassMap.get(gr.dst_obj.hkClass.name)()
                self.shape.deserialize(
                    hkFile,
                    BinaryReader(
                        initial_bytes=gr.dst_obj.bytes,
                        big_endian=hkFile.header.endian == 0,
                    ),
                    gr.dst_obj,
                )

                hkFile._assert_pointer(br)  # Points to a hkpShape
                break
        else:
            raise Exception("Something is wrong")

        self.shapeKey = br.read_uint32()
        if hkFile.header.padding_option:
            br.align_to(8)

        hkFile._assert_pointer(br)  # motion, void
        hkFile._assert_pointer(br)  # points to parent hkpCdBody

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        # Shape reference
        gr = GlobalReference()
        gr.src_obj = obj
        gr.src_rel_offset = bw.tell()
        # gr.dst_obj = HKObject()
        obj.global_references.append(gr)

        hkFile.data.objects.append(gr.dst_obj)
        hkFile._write_empty_pointer(bw)

        self.shape.serialize(
            hkFile, BinaryWriter(big_endian=hkFile.header.endian == 0), gr.dst_obj,
        )

        bw.write_uint32(UInt32(self.shapeKey))
        if hkFile.header.padding_option:
            bw.align_to(16)

        hkFile._write_empty_pointer(bw)
        hkFile._write_empty_pointer(bw)

    def as_dict(self):
        return {
            "shape": self.shape.as_dict(),
            "shapeKey": self.shapeKey,
            # "motion": self.motion,
            # "parent": self.parent,
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()

        inst.shape = class_map.HKClassMap.get(d["shape"]["hkClass"]).from_dict(
            d["shape"]
        )
        inst.shapeKey = d["shapeKey"]
        # inst.motion = d["motion"]
        # inst.parent = d["parent"]

        return inst
