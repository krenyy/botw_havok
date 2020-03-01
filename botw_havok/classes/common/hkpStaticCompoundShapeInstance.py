import botw_havok.classes.util.class_map as util

from ...binary import BinaryReader, BinaryWriter
from ...container.sections.util import GlobalReference
from ...util import QsTransform
from .hkpShape import hkpShape

if False:
    from ...hk import HK
    from ...container.sections.hkobject import HKObject


class hkpStaticCompoundShapeInstance:
    transform: QsTransform
    shape: hkpShape = None  # finish this
    filterInfo: int
    childFilterInfoMask: int
    userData: int

    def deserialize(self, hk: "HK", br: BinaryReader, obj: "HKObject"):
        self.transform = QsTransform(
            [br.read_vector4(), br.read_vector4(), br.read_vector4()]
        )

        for gr in obj.global_references:
            if gr.src_rel_offset == br.tell():
                try:
                    hk.data.objects.remove(gr.dst_obj)
                except ValueError:
                    # raise Exception
                    print(
                        "File links multiple StaticCompound instances to a single Havok object, "
                        "this is probably done to link multiple HashIds and SRTHashes to a single piece of geometry."
                        "\nThis file cannot be correctly interpreted as of yet."
                    )

                self.shape = util.HKClassMap.get(gr.dst_obj.hkclass.name)()
                self.shape.deserialize(hk, gr.dst_obj)

                hk._assert_pointer(br)
                break

        self.filterInfo = br.read_uint32()
        self.childFilterInfoMask = br.read_uint32()

        if hk.header.pointer_size == 8:
            self.userData = br.read_uint64()
        elif hk.header.pointer_size == 4:
            self.userData = br.read_uint32()
        else:
            raise NotImplementedError()

        if hk.header.padding_option:
            br.align_to(16)

    def serialize(self, hk: "HK", bw: BinaryWriter, obj: "HKObject"):
        [bw.write_vector4(v4) for v4 in self.transform]

        gr = GlobalReference()
        gr.src_obj = obj
        gr.src_rel_offset = bw.tell()
        gr.dst_section_id = 2
        gr.dst_obj = self.shape.hkobj
        gr.dst_rel_offset = 0
        obj.global_references.append(gr)
        hk.data.objects.append(self.shape.hkobj)
        self.shape.serialize(hk)

        hk._write_empty_pointer(bw)

        bw.write_uint32(self.filterInfo)
        bw.write_uint32(self.childFilterInfoMask)

        if hk.header.pointer_size == 8:
            bw.write_uint64(self.userData)
        elif hk.header.pointer_size == 4:
            bw.write_uint32(self.userData)
        else:
            raise NotImplementedError()

        if hk.header.padding_option:
            bw.align_to(16)

    def asdict(self):
        return {
            "transform": self.transform.asdict(),
            "shape": self.shape.asdict(),
            "filterInfo": self.filterInfo,
            "childFilterInfoMask": self.childFilterInfoMask,
            "userData": self.userData,
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()

        inst.transform = QsTransform.fromdict(d["transform"])
        inst.shape = util.HKClassMap.get(d["shape"]["hkClass"]).fromdict(d["shape"])
        inst.filterInfo = d["filterInfo"]
        inst.childFilterInfoMask = d["childFilterInfoMask"]
        inst.userData = d["userData"]

        return inst
