from typing import List

from ...binary import BinaryReader, BinaryWriter
from .hkLocalFrame import hkLocalFrame
from .hkpConstraintInstance import hkpConstraintInstance
from .hkpEntityExtendedListeners import hkpEntityExtendedListeners
from .hkpEntitySmallArraySerializeOverrideType import \
    hkpEntitySmallArraySerializeOverrideType
from .hkpEntitySpuCollisionCallback import hkpEntitySpuCollisionCallback
from .hkpMaterial import hkpMaterial
from .hkpMaxSizeMotion import hkpMaxSizeMotion
from .hkpWorldObject import hkpWorldObject

if False:
    from ...hk import HK
    from ...container.sections.hkobject import HKObject


class hkpEntity(hkpWorldObject):
    material: hkpMaterial
    limitContactImpulseUtilAndFlag: None = None
    damageMultiplier: float
    breakableBody: None = None

    solverData: int
    storageIndex: int
    contactPointCallbackDelay: int

    constraintsMaster: hkpEntitySmallArraySerializeOverrideType
    constraintsSlave: List[hkpConstraintInstance]
    constraintRuntime: List[int]

    simulationIsland: None = None

    autoRemoveLevel: int
    numShapeKeysInContactPointProperties: int
    responseModifierFlags: int

    uid: int

    spuCollisionCallback: hkpEntitySpuCollisionCallback
    motion: hkpMaxSizeMotion
    contactListeners: hkpEntitySmallArraySerializeOverrideType
    actions: hkpEntitySmallArraySerializeOverrideType
    localFrame: hkLocalFrame = None  # Pointer
    extendedListeners: hkpEntityExtendedListeners = None  # Pointer

    npData: int

    def __init__(self):
        super().__init__()

        self.constraintsSlave = []
        self.constraintRuntime = []

    def deserialize(self, hk: "HK", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hk, br, obj)

        self.material = hkpMaterial()
        self.material.deserialize(hk, br)

        if hk.header.padding_option:
            br.align_to(16)

        limitContactImpulseUtilAndFlag_offset = br.tell()
        hk._assert_pointer(br)  # limitContactImpulseUtilAndFlag

        self.damageMultiplier = br.read_single()

        if hk.header.padding_option:
            br.align_to(16)

        breakableBody_offset = br.tell()
        hk._assert_pointer(br)  # breakableBody

        self.solverData = br.read_uint32()

        self.storageIndex = br.read_uint16()
        self.contactPointCallbackDelay = br.read_uint16()

        self.constraintsMaster = hkpEntitySmallArraySerializeOverrideType()
        self.constraintsMaster.deserialize(hk, br)

        constraintsSlaveCount_offset = br.tell()
        constraintsSlaveCount = hk._read_counter(br)

        constraintRuntimeCount_offset = br.tell()
        constraintRuntimeCount = hk._read_counter(br)

        simulationIsland_offset = br.tell()
        hk._assert_pointer(br)  # simulationIsland

        # ----

        self.autoRemoveLevel = br.read_int8()
        self.numShapeKeysInContactPointProperties = br.read_uint8()
        self.responseModifierFlags = br.read_uint8()
        br.read_uint8()  # Padding

        self.uid = br.read_uint32()

        self.spuCollisionCallback = hkpEntitySpuCollisionCallback()
        self.spuCollisionCallback.deserialize(hk, br)

        self.motion = hkpMaxSizeMotion()
        self.motion.deserialize(hk, br)

        self.contactListeners = hkpEntitySmallArraySerializeOverrideType()
        self.contactListeners.deserialize(hk, br)

        self.actions = hkpEntitySmallArraySerializeOverrideType()
        self.actions.deserialize(hk, br)

        # ----

        localFrame_offset = br.tell()
        hk._assert_pointer(br)  # localFrame

        extendedListeners = br.tell()
        hk._assert_pointer(br)  # extendedListeners

        # ----

        self.npData = br.read_uint32()

        # TODO: CONSTRAINTS
        # FIXME: Put those at the end of RigidBody
        """for _ in range(constraintsSlaveCount):
            constr = hkpConstraintInstance()
            constr.deserialize(hk, br)
            self.constraintsSlave.append(constr)

        for _ in range(constraintRuntimeCount):
            self.constraintRuntime.append(br.read_uint8())"""

    def serialize(self, hk: "HK", bw: BinaryWriter):
        super().serialize(hk, bw)

        self.material.serialize(hk, bw)

        if hk.header.padding_option:
            bw.align_to(16)

        limitContactImpulseUtilAndFlag_offset = bw.tell()
        hk._write_empty_pointer(bw)  # limitContactImpulseUtilAndFlag

        bw.write_single(self.damageMultiplier)

        if hk.header.padding_option:
            bw.align_to(16)

        breakableBody_offset = bw.tell()
        hk._write_empty_pointer(bw)  # breakableBody

        bw.write_uint32(self.solverData)

        bw.write_uint16(self.storageIndex)
        bw.write_uint16(self.contactPointCallbackDelay)

        self.constraintsMaster.serialize(hk, bw)

        constraintsSlaveCount_offset = bw.tell()
        hk._write_counter(bw, len(self.constraintsSlave))

        constraintRuntimeCount_offset = bw.tell()
        hk._write_counter(bw, len(self.constraintRuntime))

        simulationIsland_offset = bw.tell()
        hk._write_empty_pointer(bw)  # simulationIsland

        # ----

        bw.write_int8(self.autoRemoveLevel)
        bw.write_int8(self.numShapeKeysInContactPointProperties)
        bw.write_int8(self.responseModifierFlags)
        bw.write_uint8(0x0)  # Padding

        bw.write_uint32(self.uid)

        self.spuCollisionCallback.serialize(hk, bw)
        self.motion.serialize(hk, bw)
        self.contactListeners.serialize(hk, bw)
        self.actions.serialize(hk, bw)

        # ----

        localFrame_offset = bw.tell()
        hk._write_empty_pointer(bw)  # localFrame

        extendedListeners = bw.tell()
        hk._write_empty_pointer(bw)  # extendedListeners

        # ----

        bw.write_uint32(self.npData)
