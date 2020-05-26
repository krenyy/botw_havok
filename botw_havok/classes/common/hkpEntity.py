from typing import TYPE_CHECKING

from .hkpEntitySmallArraySerializeOverrideType import (
    hkpEntitySmallArraySerializeOverrideType,
)
from .hkpEntitySpuCollisionCallback import hkpEntitySpuCollisionCallback
from .hkpMaterial import hkpMaterial
from .hkpMaxSizeMotion import hkpMaxSizeMotion
from .hkpWorldObject import hkpWorldObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Float32, Int8, UInt8, UInt16, UInt32
from ...container.util.localfixup import LocalFixup

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpEntity(hkpWorldObject):
    material: hkpMaterial
    # limitContactImpulseUtilAndFlag: None = None
    damageMultiplier: Float32
    # breakableBody: None = None

    solverData: UInt32
    storageIndex: UInt16
    contactPointCallbackDelay: UInt16

    constraintsMaster: hkpEntitySmallArraySerializeOverrideType
    # constraintsSlave: List[hkpConstraintInstance]
    # constraintRuntime: List[int]

    # simulationIsland: None = None

    autoRemoveLevel: Int8
    numShapeKeysInContactPointProperties: UInt8
    responseModifierFlags: UInt8

    uid: UInt32

    spuCollisionCallback: hkpEntitySpuCollisionCallback
    motion: hkpMaxSizeMotion
    contactListeners: hkpEntitySmallArraySerializeOverrideType
    actions: hkpEntitySmallArraySerializeOverrideType
    # localFrame: hkLocalFrame = None  # Pointer
    # extendedListeners: hkpEntityExtendedListeners = None  # Pointer

    npData: UInt32

    def __init__(self):
        super().__init__()

        self.constraintsSlave = []
        self.constraintRuntime = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        ###

        self.material = hkpMaterial()
        self.material.deserialize(hkFile, br, obj)

        if hkFile.header.padding_option:
            br.align_to(8)

        hkFile._assert_pointer(br)  # limitContactImpulseUtilAndFlag

        self.damageMultiplier = br.read_float32()

        if hkFile.header.padding_option:
            br.align_to(8)

        hkFile._assert_pointer(br)  # breakableBody

        self.solverData = br.read_uint32()

        self.storageIndex = br.read_uint16()
        self.contactPointCallbackDelay = br.read_uint16()

        self.constraintsMaster = hkpEntitySmallArraySerializeOverrideType()
        self.constraintsMaster.deserialize(hkFile, br, obj)

        constraintsSlaveCount_offset = hkFile._assert_pointer(br)
        constraintsSlaveCount = hkFile._read_counter(br)
        assert constraintsSlaveCount == 0

        constraintRuntimeCount_offset = hkFile._assert_pointer(br)
        constraintRuntimeCount = hkFile._read_counter(br)
        assert constraintRuntimeCount == 0

        hkFile._assert_pointer(br)  # simulationIsland

        # ----

        self.autoRemoveLevel = br.read_int8()
        self.numShapeKeysInContactPointProperties = br.read_uint8()
        self.responseModifierFlags = br.read_uint8()
        br.align_to(2)

        self.uid = br.read_uint32()

        self.spuCollisionCallback = hkpEntitySpuCollisionCallback()
        self.spuCollisionCallback.deserialize(hkFile, br, obj)

        br.align_to(16)

        self.motion = hkpMaxSizeMotion()
        self.motion.deserialize(hkFile, br, obj)

        if hkFile.header.padding_option:
            br.align_to(16)

        self.contactListeners = hkpEntitySmallArraySerializeOverrideType()
        self.contactListeners.deserialize(hkFile, br, obj)

        self.actions = hkpEntitySmallArraySerializeOverrideType()
        self.actions.deserialize(hkFile, br, obj)

        hkFile._assert_pointer(br)  # localFrame

        hkFile._assert_pointer(br)  # extendedListeners

        self.npData = br.read_uint32()

        br.align_to(16)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        self.material.serialize(hkFile, bw, obj)

        if hkFile.header.padding_option:
            bw.align_to(8)

        limitContactImpulseUtilAndFlag_offset = hkFile._write_empty_pointer(bw)

        bw.write_float32(self.damageMultiplier)

        if hkFile.header.padding_option:
            bw.align_to(8)

        breakableBody_offset = hkFile._write_empty_pointer(bw)

        bw.write_uint32(self.solverData)

        bw.write_uint16(self.storageIndex)
        bw.write_uint16(self.contactPointCallbackDelay)

        self.constraintsMaster.serialize(hkFile, bw, obj)

        constraintsSlaveCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.constraintsSlave)))

        constraintRuntimeCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.constraintRuntime)))

        simulationIsland_offset = hkFile._write_empty_pointer(bw)

        # ----

        bw.write_int8(self.autoRemoveLevel)
        bw.write_uint8(self.numShapeKeysInContactPointProperties)
        bw.write_uint8(self.responseModifierFlags)
        bw.align_to(2)

        bw.write_uint32(self.uid)

        self.spuCollisionCallback.serialize(hkFile, bw, obj)

        bw.align_to(16)

        self.motion.serialize(hkFile, bw, obj)

        if hkFile.header.padding_option:
            bw.align_to(16)

        self.contactListeners.serialize(hkFile, bw, obj)
        self.actions.serialize(hkFile, bw, obj)

        # ----

        localFrame_offset = hkFile._write_empty_pointer(bw)  # localFrame

        extendedListeners = hkFile._write_empty_pointer(bw)  # extendedListeners

        # ----

        bw.write_uint32(self.npData)
        bw.align_to(16)

        ####################
        # Write array data #
        ####################

        obj.local_fixups.append(LocalFixup(self._namePointer_offset, bw.tell()))

        bw.write_string(self.name)
        bw.align_to(16)

    def as_dict(self):
        d = super().as_dict()
        d.update(
            {
                "material": self.material.as_dict(),
                "damageMultiplier": self.damageMultiplier,
                "solverData": self.solverData,
                "storageIndex": self.storageIndex,
                "contactPointCallbackDelay": self.contactPointCallbackDelay,
                "constraintsMaster": self.constraintsMaster.as_dict(),
                # "constraintsSlave": [slave.as_dict() for slave in self.constraintsSlave],
                # "constraintRuntime": self.constraintRuntime,
                "autoRemoveLevel": self.autoRemoveLevel,
                "numShapeKeysInContactPointProperties": self.numShapeKeysInContactPointProperties,
                "responseModifierFlags": self.responseModifierFlags,
                "uid": self.uid,
                "spuCollisionCallback": self.spuCollisionCallback.as_dict(),
                "motion": self.motion.as_dict(),
                "contactListeners": self.contactListeners.as_dict(),
                "actions": self.actions.as_dict(),
                "npData": self.npData,
            }
        )
        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().from_dict(d).__dict__)

        inst.material = hkpMaterial.from_dict(d["material"])
        inst.damageMultiplier = d["damageMultiplier"]
        inst.solverData = d["solverData"]
        inst.storageIndex = d["storageIndex"]
        inst.contactPointCallbackDelay = d["contactPointCallbackDelay"]
        inst.constraintsMaster = hkpEntitySmallArraySerializeOverrideType.from_dict(
            d["constraintsMaster"]
        )
        # inst.constraintsSlave = [hkpConstraintInstance.from_dict(slave) for slave in d["constraintsSlave"]]
        # inst.constraintRuntime = d["constraintRuntime"]
        inst.autoRemoveLevel = d["autoRemoveLevel"]
        inst.numShapeKeysInContactPointProperties = d[
            "numShapeKeysInContactPointProperties"
        ]
        inst.responseModifierFlags = d["responseModifierFlags"]
        inst.uid = d["uid"]
        inst.spuCollisionCallback = hkpEntitySpuCollisionCallback.from_dict(
            d["spuCollisionCallback"]
        )
        inst.motion = hkpMaxSizeMotion.from_dict(d["motion"])
        inst.contactListeners = hkpEntitySmallArraySerializeOverrideType.from_dict(
            d["contactListeners"]
        )
        inst.actions = hkpEntitySmallArraySerializeOverrideType.from_dict(d["actions"])
        inst.npData = d["npData"]

        return inst
