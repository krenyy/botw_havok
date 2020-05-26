from typing import TYPE_CHECKING

import botw_havok.classes.util.class_map as class_map
from .hkObject import hkObject
from ..base import HKBaseClass
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Int16, Int32, UInt16, UInt32
from ...container.util.globalreference import GlobalReference

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpListShapeChildInfo(hkObject):
    shape: HKBaseClass
    collisionFilterInfo: UInt32
    shapeInfo: UInt16
    shapeSize: Int16
    numChildShapes: Int32

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        shape_offset = hkFile._assert_pointer(br)

        self.collisionFilterInfo = br.read_uint32()
        self.shapeInfo = br.read_uint16()
        self.shapeSize = br.read_int16()
        self.numChildShapes = br.read_int32()

        br.align_to(16)

        for gr in obj.global_references:
            if gr.src_rel_offset == shape_offset:
                try:
                    hkFile.data.objects.remove(gr.dst_obj)
                except ValueError:
                    pass

                self.shape = class_map.HKClassMap.get(gr.dst_obj.hkClass.name)()
                self.shape.deserialize(
                    hkFile,
                    BinaryReader(
                        initial_bytes=gr.dst_obj.bytes,
                        big_endian=hkFile.header.endian == 0,
                    ),
                    gr.dst_obj,
                )

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        shape_offset = hkFile._write_empty_pointer(bw)

        bw.write_uint32(self.collisionFilterInfo)
        bw.write_uint16(self.shapeInfo)
        bw.write_int16(self.shapeSize)
        bw.write_int32(self.numChildShapes)

        bw.align_to(16)

        gr = GlobalReference()
        gr.src_obj = obj
        gr.src_rel_offset = shape_offset
        gr.dst_section_id = Int32(2)
        obj.global_references.append(gr)

        self.shape.serialize(
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

    def as_dict(self):
        return {
            "shape": self.shape.as_dict(),
            "collisionFilterInfo": self.collisionFilterInfo,
            "shapeInfo": self.shapeInfo,
            "shapeSize": self.shapeSize,
            "numChildShapes": self.numChildShapes,
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(
            {
                "shape": class_map.HKClassMap.get(d["shape"]["hkClass"]).from_dict(
                    d["shape"]
                ),
                "collisionFilterInfo": d["collisionFilterInfo"],
                "shapeInfo": d["shapeInfo"],
                "shapeSize": d["shapeSize"],
                "numChildShapes": d["numChildShapes"],
            }
        )

        return inst
