from ..binary import BinaryReader, BinaryWriter
from .base import HKBase
from .common.hkReferencedObject import hkReferencedObject
from typing import List

if False:
    from ..hk import HK
    from ..container.sections.hkobject import HKObject


class hkpPhysicsSystem(HKBase, hkReferencedObject):
    """Physics system, contains rigid bodies
    """

    # rigidBodies: List[hkpRigidBody]
    # constraints: List[hkpConstraintInstance] # TODO: Do this
    # actions: List[hkpAction] # Doesn't seem used
    # phantoms: List[hkpPhantom] # Doesn't seem used

    name: str
    userData: int
    active: bool

    def deserialize(self, hk: "HK", obj: "HKObject"):
        HKBase.deserialize(self, hk, obj)

        br = BinaryReader(self.hkobj.bytes)
        br.big_endian = hk.header.endian == 0

        hkReferencedObject.deserialize(self, hk, br)

        # ---

        rigidBodiesCount_offset = br.tell()
        rigidBodiesCount = self.read_counter(hk, br)

        constraintsCount_offset = br.tell()
        constraintsCount = self.read_counter(hk, br)

        actionsCount_offset = br.tell()
        actionsCount = self.read_counter(hk, br)

        phantomsCount_offset = br.tell()
        phantomsCount = self.read_counter(hk, br)

        namePointer_offset = br.tell()
        hk._assert_pointer(br)

        self.userData = br.read_uint64()
        self.active = bool(br.read_int8())
        br.align_to(16)

        # ---

        pass

    def serialize(self, hk: "HK"):
        bw = BinaryWriter()
        bw.big_endian = hk.header.endian == 0

        hkReferencedObject.serialize(self, hk, bw)

        pass

        HKBase.serialize(self, hk, bw)
