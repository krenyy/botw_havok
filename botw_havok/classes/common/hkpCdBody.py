from .hkpShape import hkpShape
from ...binary import BinaryReader, BinaryWriter
import botw_havok.classes.util.class_map as util
from ...container.sections.util import GlobalReference

if False:
    from ...hk import HK
    from ...container.sections.hkobject import HKObject


class hkpCdBody:
    shape: hkpShape
    shapeKey: int
    # motion: None = None
    # parent: "hkpCdBody" = None

    def deserialize(self, hk: "HK", br: BinaryReader, obj: "HKObject"):
        for gr in obj.global_references:
            if gr.src_rel_offset == br.tell():
                hk.data.objects.remove(gr.dst_obj)
                self.shape = util.HKClassMap.get(gr.dst_obj.hkclass.name)()
                self.shape.deserialize(hk, gr.dst_obj)

                hk._assert_pointer(br)  # Points to a hkpShape
                break
        else:
            raise Exception("Something is wrong")

        self.shapeKey = br.read_uint32()
        if hk.header.padding_option:
            br.align_to(8)

        hk._assert_pointer(br)  # motion, void
        hk._assert_pointer(br)  # points to parent hkpCdBody

    def serialize(self, hk: "HK", bw: BinaryWriter, obj: "HKObject"):
        # Shape reference
        gr = GlobalReference()
        gr.src_obj = obj
        gr.src_rel_offset = bw.tell()
        gr.dst_obj = self.shape.hkobj
        obj.global_references.append(gr)

        hk.data.objects.append(self.shape.hkobj)
        self.shape.serialize(hk)

        hk._write_empty_pointer(bw)

        bw.write_uint32(self.shapeKey)
        if hk.header.padding_option:
            bw.align_to(16)

        hk._write_empty_pointer(bw)
        hk._write_empty_pointer(bw)

    def asdict(self):
        return {
            "shape": self.shape.asdict(),
            "shapeKey": self.shapeKey,
            # "motion": self.motion,
            # "parent": self.parent,
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()

        inst.shape = util.HKClassMap.get(d["shape"]["hkClass"]).fromdict(d["shape"])
        inst.shapeKey = d["shapeKey"]
        # inst.motion = d["motion"]
        # inst.parent = d["parent"]

        return inst
