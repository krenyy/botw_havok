from typing import TYPE_CHECKING

from .base import HKBaseClass
from .common.hkaiNavMeshQueryMediator import hkaiNavMeshQueryMediator
from ..binary import BinaryReader, BinaryWriter
from ..container.util.globalreference import GlobalReference

if TYPE_CHECKING:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkaiStaticTreeNavMeshQueryMediator(HKBaseClass, hkaiNavMeshQueryMediator):
    tree: str  # hkcdStaticAabbTree
    navMesh: str  # hkaiNavMesh

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        HKBaseClass.deserialize(self, hkFile, br, obj)
        hkaiNavMeshQueryMediator.deserialize(self, hkFile, br, obj)

        if hkFile.header.padding_option:
            br.align_to(16)

        self.tree = "->hkcdStaticAabbTree"
        self.navMesh = "-> hkaiNavMesh"

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        HKBaseClass.assign_class(self, hkFile, obj)
        hkaiNavMeshQueryMediator.serialize(self, hkFile, bw, obj)

        if hkFile.header.padding_option:
            bw.align_to(16)

        gr = GlobalReference()
        gr.src_obj = obj
        gr.src_rel_offset = hkFile._write_empty_pointer(bw)
        gr.dst_obj = obj
        gr.dst_rel_offset = bw.tell() + hkFile.header.pointer_size

        obj.global_references.append(gr)

        for o in hkFile.data.objects:
            if o.hkClass.name == "hkaiNavMesh":
                gr = GlobalReference()
                gr.src_obj = obj
                gr.src_rel_offset = hkFile._write_empty_pointer(bw)
                gr.dst_obj = o

                obj.global_references.append(gr)

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def as_dict(self):
        d = HKBaseClass.as_dict(self)
        d.update(hkaiNavMeshQueryMediator.as_dict(self))
        d.update(
            {"tree": "->hkcdStaticAabbTree", "navMesh": "->hkaiNavMesh", }
        )
        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBaseClass.from_dict(d).__dict__)
        inst.__dict__.update(hkaiNavMeshQueryMediator.from_dict(d).__dict__)

        inst.tree = d["tree"]
        inst.navMesh = d["navMesh"]

        return inst
