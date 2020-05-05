from typing import List, Union

from ..binary import BinaryReader, BinaryWriter
from ..binary.types import Bool, Int8, String, UInt32, UInt64
from ..container.util.globalreference import GlobalReference
from ..container.util.localfixup import LocalFixup
from .base import HKBaseClass
from .common.hkReferencedObject import hkReferencedObject
from .hkpRigidBody import hkpRigidBody

if False:
    from ..hkfile import HKFile
    from ..container.util.hkobject import HKObject


class hkpPhysicsSystem(HKBaseClass, hkReferencedObject):
    """Physics system, contains rigid bodies
    """

    rigidBodies: List[hkpRigidBody]
    # constraints: List[hkpConstraintInstance]  # Might be used in cloth or ragdoll files, not sure yet
    # actions: List[hkpAction]  # Looks unused
    # phantoms: List[hkpPhantom]  # Looks unused

    name: String
    userData: Union[UInt32, UInt64]
    active: Bool

    def __init__(self):
        super().__init__()

        self.rigidBodies = []
        self.constraints = []
        self.actions = []
        self.phantoms = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        HKBaseClass.deserialize(self, hkFile, br, obj)
        hkReferencedObject.deserialize(self, hkFile, br, obj)

        ###

        if hkFile.header.padding_option:
            br.align_to(16)

        rigidBodiesCount_offset = hkFile._assert_pointer(br)
        rigidBodiesCount = hkFile._read_counter(br)

        constraintsCount_offset = hkFile._assert_pointer(br)
        constraintsCount = hkFile._read_counter(br)

        actionsCount_offset = hkFile._assert_pointer(br)
        actionsCount = hkFile._read_counter(br)

        phantomsCount_offset = hkFile._assert_pointer(br)
        phantomsCount = hkFile._read_counter(br)

        namePointer_offset = hkFile._assert_pointer(br)

        # ----

        if hkFile.header.pointer_size == 8:
            self.userData = br.read_uint64()
        elif hkFile.header.pointer_size == 4:
            self.userData = br.read_uint32()
        else:
            raise NotImplementedError()

        self.active = Bool(br.read_int8())
        br.align_to(16)

        # ----

        for gr in obj.global_references:
            if gr.src_rel_offset == br.tell():
                hkFile.data.objects.remove(gr.dst_obj)

                rb = hkpRigidBody()
                self.rigidBodies.append(rb)
                rb.deserialize(
                    hkFile,
                    BinaryReader(
                        initial_bytes=gr.dst_obj.bytes,
                        big_endian=hkFile.header.endian == 0,
                    ),
                    gr.dst_obj,
                )

                hkFile._assert_pointer(br)
        br.align_to(16)

        self.name = br.read_string()
        br.align_to(16)

        obj.local_fixups.clear()
        obj.global_references.clear()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        HKBaseClass.assign_class(self, hkFile, obj)
        hkReferencedObject.serialize(self, hkFile, bw, obj)

        ###

        if hkFile.header.padding_option:
            bw.align_to(16)

        rigidBodiesCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.rigidBodies)))

        constraintsCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.constraints)))

        actionsCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.actions)))

        phantomsCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.phantoms)))

        namePointer_offset = hkFile._write_empty_pointer(bw)

        ###

        if hkFile.header.pointer_size == 8:
            bw.write_uint64(UInt64(self.userData))
        elif hkFile.header.pointer_size == 4:
            bw.write_uint32(UInt32(self.userData))
        else:
            raise NotImplementedError("idk really")

        bw.write_int8(Int8(self.active))
        bw.align_to(16)

        ##############
        # Write data #
        ##############

        if self.rigidBodies:
            obj.local_fixups.append(LocalFixup(rigidBodiesCount_offset, bw.tell()))

            for rb in self.rigidBodies:
                gr = GlobalReference()
                gr.src_obj = obj
                gr.src_rel_offset = bw.tell()
                obj.global_references.append(gr)

                hkFile._write_empty_pointer(bw)
                hkFile.data.objects.append(gr.dst_obj)

                rb.serialize(
                    hkFile,
                    BinaryWriter(big_endian=hkFile.header.endian == 0),
                    gr.dst_obj,
                )

            bw.align_to(16)

        obj.local_fixups.append(LocalFixup(namePointer_offset, bw.tell()))
        bw.write_string(self.name)
        bw.align_to(16)

        ###

        HKBaseClass.serialize(self, hkFile, bw, obj)

    def asdict(self):
        d = HKBaseClass.asdict(self)
        d.update(hkReferencedObject.asdict(self))
        d.update(
            {
                "rigidBodies": [rb.asdict() for rb in self.rigidBodies],
                # "constraints": [c.asdict() for c in self.constraints],
                # "actions": [a.asdict() for a in self.actions],
                # "phantoms": [p.asdict() for p in self.phantoms],
                "name": self.name,
                "userData": self.userData,
                "active": bool(self.active),
            }
        )
        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(HKBaseClass.fromdict(d).__dict__)
        inst.__dict__.update(hkReferencedObject.fromdict(d).__dict__)

        inst.rigidBodies = [hkpRigidBody.fromdict(rb) for rb in d["rigidBodies"]]
        # inst.constraints = [hkpConstraintInstance.fromdict(c) for c in d["constraints"]]
        inst.name = d["name"]
        inst.userData = d["userData"]
        inst.active = Bool(d["active"])

        return inst

    def __repr__(self):
        return "<{}({}, {}, {}, {})>".format(
            self.__class__.__name__,
            self.name,
            self.active,
            self.rigidBodies,
            self.userData,
        )
