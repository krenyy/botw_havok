from typing import List

from ...binary import BinaryReader, BinaryWriter
from ...container.sections.util import LocalFixup
from .hkLocalFrame import hkLocalFrame
from .hkMultiThreadCheck import hkMultiThreadCheck
from .hkpConstraintInstance import hkpConstraintInstance
from .hkpEntityExtendedListeners import hkpEntityExtendedListeners
from .hkpEntitySmallArraySerializeOverrideType import (
    hkpEntitySmallArraySerializeOverrideType,
)
from .hkpEntitySpuCollisionCallback import hkpEntitySpuCollisionCallback
from .hkpLinkedCollidable import hkpLinkedCollidable
from .hkpMaterial import hkpMaterial
from .hkpMaxSizeMotion import hkpMaxSizeMotion
from .hkpWorldObject import hkpWorldObject

if False:
    from ...hk import HK
    from ...container.sections.hkobject import HKObject


class hkpEntity(hkpWorldObject):
    material: hkpMaterial
    # limitContactImpulseUtilAndFlag: None = None
    damageMultiplier: float
    # breakableBody: None = None

    solverData: int
    storageIndex: int
    contactPointCallbackDelay: int

    constraintsMaster: hkpEntitySmallArraySerializeOverrideType
    # constraintsSlave: List[hkpConstraintInstance]
    # constraintRuntime: List[int]

    # simulationIsland: None = None

    autoRemoveLevel: int
    numShapeKeysInContactPointProperties: int
    responseModifierFlags: int

    uid: int

    spuCollisionCallback: hkpEntitySpuCollisionCallback
    motion: hkpMaxSizeMotion
    contactListeners: hkpEntitySmallArraySerializeOverrideType
    actions: hkpEntitySmallArraySerializeOverrideType
    # localFrame: hkLocalFrame = None  # Pointer
    # extendedListeners: hkpEntityExtendedListeners = None  # Pointer

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
            br.align_to(8)

        limitContactImpulseUtilAndFlag_offset = br.tell()
        hk._assert_pointer(br)  # limitContactImpulseUtilAndFlag

        self.damageMultiplier = br.read_single()

        if hk.header.padding_option:
            br.align_to(8)

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
        br.align_to(2)

        self.uid = br.read_uint32()

        self.spuCollisionCallback = hkpEntitySpuCollisionCallback()
        self.spuCollisionCallback.deserialize(hk, br)

        br.align_to(16)  # TODO: Check if this is correct

        self.motion = hkpMaxSizeMotion()
        self.motion.deserialize(hk, br)

        if hk.header.padding_option:
            br.align_to(16)  # TODO: Check if right

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

        br.align_to(16)  # Should be right

        # TODO: Figure out, what do the commented structs do and read them

    def serialize(self, hk: "HK", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hk, bw, obj)

        self.material.serialize(hk, bw)

        if hk.header.padding_option:
            bw.align_to(8)

        limitContactImpulseUtilAndFlag_offset = bw.tell()
        hk._write_empty_pointer(bw)  # limitContactImpulseUtilAndFlag

        bw.write_single(self.damageMultiplier)

        if hk.header.padding_option:
            bw.align_to(8)

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
        bw.align_to(2)

        bw.write_uint32(self.uid)

        self.spuCollisionCallback.serialize(hk, bw)

        bw.align_to(16)  # TODO: Check if correct

        self.motion.serialize(hk, bw)

        if hk.header.padding_option:
            bw.align_to(16)

        self.contactListeners.serialize(hk, bw)
        self.actions.serialize(hk, bw)

        # ----

        localFrame_offset = bw.tell()
        hk._write_empty_pointer(bw)  # localFrame

        extendedListeners = bw.tell()
        hk._write_empty_pointer(bw)  # extendedListeners

        # ----

        bw.write_uint32(self.npData)
        bw.align_to(16)

        name_offset = bw.tell()
        bw.write_string(self.name)
        bw.align_to(16)

        obj.local_fixups.append(LocalFixup(self._namePointer_offset, name_offset))

    def asdict(self):
        d = super().asdict()
        d.update(
            {
                "material": self.material.asdict(),
                "damageMultiplier": self.damageMultiplier,
                "solverData": self.solverData,
                "storageIndex": self.storageIndex,
                "contactPointCallbackDelay": self.contactPointCallbackDelay,
                "constraintsMaster": self.constraintsMaster.asdict(),
                # "constraintsSlave": [slave.asdict() for slave in self.constraintsSlave],
                # "constraintRuntime": self.constraintRuntime,
                "autoRemoveLevel": self.autoRemoveLevel,
                "numShapeKeysInContactPointProperties": self.numShapeKeysInContactPointProperties,
                "responseModifierFlags": self.responseModifierFlags,
                "uid": self.uid,
                "spuCollisionCallback": self.spuCollisionCallback.asdict(),
                "motion": self.motion.asdict(),
                "contactListeners": self.contactListeners.asdict(),
                "actions": self.actions.asdict(),
                "npData": self.npData,
            }
        )
        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.material = hkpMaterial.fromdict(d["material"])
        inst.damageMultiplier = d["damageMultiplier"]
        inst.solverData = d["solverData"]
        inst.storageIndex = d["storageIndex"]
        inst.contactPointCallbackDelay = d["contactPointCallbackDelay"]
        inst.constraintsMaster = hkpEntitySmallArraySerializeOverrideType.fromdict(
            d["constraintsMaster"]
        )
        # inst.constraintsSlave = [hkpConstraintInstance.fromdict(slave) for slave in d["constraintsSlave"]]
        # inst.constraintRuntime = d["constraintRuntime"]
        inst.autoRemoveLevel = d["autoRemoveLevel"]
        inst.numShapeKeysInContactPointProperties = d[
            "numShapeKeysInContactPointProperties"
        ]
        inst.responseModifierFlags = d["responseModifierFlags"]
        inst.uid = d["uid"]
        inst.spuCollisionCallback = hkpEntitySpuCollisionCallback.fromdict(
            d["spuCollisionCallback"]
        )
        inst.motion = hkpMaxSizeMotion.fromdict(d["motion"])
        inst.contactListeners = hkpEntitySmallArraySerializeOverrideType.fromdict(
            d["contactListeners"]
        )
        inst.actions = hkpEntitySmallArraySerializeOverrideType.fromdict(d["actions"])
        inst.npData = d["npData"]

        return inst
