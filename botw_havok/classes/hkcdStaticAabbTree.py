from typing import TYPE_CHECKING

from .base import HKBaseClass
from .common.hkReferencedObject import hkReferencedObject
from ..binary import BinaryReader, BinaryWriter
from ..binary.types import UInt8
from ..container.util.globalreference import GlobalReference

if TYPE_CHECKING:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkcdStaticAabbTree(HKBaseClass, hkReferencedObject):
    shouldDeleteTree: bool
    treePtr: str  # hkcdStaticTreeDefaultTreeStorage6

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        HKBaseClass.deserialize(self, hkFile, br, obj)
        hkReferencedObject.deserialize(self, hkFile, br, obj)

        self.shouldDeleteTree = bool(br.read_uint8())
        self.treePtr = "->hkcdStaticTreeDefaultTreeStorage6"

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        HKBaseClass.assign_class(self, hkFile, obj)
        hkReferencedObject.serialize(self, hkFile, bw, obj)

        bw.write_uint8(UInt8(self.shouldDeleteTree))
        bw.align_to(4)

        gr = GlobalReference()
        gr.src_rel_offset = hkFile._write_empty_pointer(bw)
        gr.src_obj = obj
        gr.dst_obj = obj

        bw.align_to(16)

        gr.dst_rel_offset = bw.tell()  # WORKAROUND
        obj.global_references.append(gr)

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def as_dict(self):
        d = HKBaseClass.as_dict(self)
        d.update(hkReferencedObject.as_dict(self))
        d.update(
            {"shouldDeleteTree": self.shouldDeleteTree, "treePtr": self.treePtr, }
        )

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBaseClass.from_dict(d).__dict__)
        inst.__dict__.update(hkReferencedObject.from_dict(d).__dict__)

        inst.shouldDeleteTree = d["shouldDeleteTree"]
        inst.treePtr = d["treePtr"]

        return inst
