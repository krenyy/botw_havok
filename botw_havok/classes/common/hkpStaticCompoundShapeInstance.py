from typing import TYPE_CHECKING
from typing import Union

import botw_havok.classes.util.class_map as class_map
from .hkObject import hkObject
from ..base import HKBaseClass
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Int32, Matrix, UInt32, UInt64
from ...container.util.globalreference import GlobalReference

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpStaticCompoundShapeInstance(hkObject):
    transform: Matrix
    shape: HKBaseClass
    filterInfo: UInt32
    childFilterInfoMask: UInt32
    userData: Union[UInt32, UInt64]

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.transform = br.read_matrix(3)

        for gr in obj.global_references:
            if gr.src_rel_offset == br.tell():
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

                hkFile._assert_pointer(br)
                break

        self.filterInfo = br.read_uint32()
        self.childFilterInfoMask = br.read_uint32()

        if hkFile.header.pointer_size == 8:
            self.userData = br.read_uint64()
        elif hkFile.header.pointer_size == 4:
            self.userData = br.read_uint32()
        else:
            raise NotImplementedError()

        if hkFile.header.padding_option:
            br.align_to(16)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_matrix(self.transform)

        gr = GlobalReference()
        gr.src_obj = obj
        gr.src_rel_offset = bw.tell()
        gr.dst_section_id = Int32(2)
        gr.dst_rel_offset = UInt32(0)
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

        hkFile._write_empty_pointer(bw)

        bw.write_uint32(self.filterInfo)
        bw.write_uint32(self.childFilterInfoMask)

        if hkFile.header.pointer_size == 8:
            bw.write_uint64(UInt64(self.userData))
        elif hkFile.header.pointer_size == 4:
            bw.write_uint32(UInt32(self.userData))
        else:
            raise NotImplementedError()

        if hkFile.header.padding_option:
            bw.align_to(16)

    def as_dict(self):
        return {
            "transform": self.transform.as_dict(),
            "shape": self.shape.as_dict(),
            "filterInfo": self.filterInfo,
            "childFilterInfoMask": self.childFilterInfoMask,
            "userData": self.userData,
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()

        inst.transform = Matrix.from_dict(d["transform"])
        inst.shape = class_map.HKClassMap.get(d["shape"]["hkClass"]).from_dict(
            d["shape"]
        )
        inst.filterInfo = d["filterInfo"]
        inst.childFilterInfoMask = d["childFilterInfoMask"]
        inst.userData = d["userData"]

        return inst
