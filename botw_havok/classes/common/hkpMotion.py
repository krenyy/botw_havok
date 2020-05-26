from typing import List
from typing import TYPE_CHECKING

from .hkMotionState import hkMotionState
from .hkReferencedObject import hkReferencedObject
from ..enums.MotionType import MotionType
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Float16, UInt8, UInt16, UInt32, Vector4

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpMotion(hkReferencedObject):
    type: UInt8
    deactivationIntegrateCounter: UInt8
    deactivationNumInactiveFrames: List[UInt16]

    motionState: hkMotionState

    inertiaAndMassInv: Vector4

    linearVelocity: Vector4
    angularVelocity: Vector4

    deactivationRefPosition: List[Vector4]
    deactivationRefOrientation: UInt32

    # savedMotion: "hkpMaxSizeMotion" = None
    savedQualityTypeIndex: UInt16

    gravityFactor: Float16

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        ###

        self.type = br.read_uint8()
        self.deactivationIntegrateCounter = br.read_uint8()
        self.deactivationNumInactiveFrames = [br.read_uint16() for _ in range(2)]

        br.align_to(16)

        self.motionState = hkMotionState()
        self.motionState.deserialize(hkFile, br, obj)

        self.inertiaAndMassInv = br.read_vector4()

        self.linearVelocity = br.read_vector4()
        self.angularVelocity = br.read_vector4()

        self.deactivationRefPosition = [br.read_vector4() for _ in range(2)]
        self.deactivationRefOrientation = br.read_uint32()

        br.align_to(8)

        savedMotion_offset = hkFile._assert_pointer(br)

        self.savedQualityTypeIndex = br.read_uint16()

        self.gravityFactor = br.read_float16()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        ###

        bw.write_uint8(UInt8(self.type))
        bw.write_uint8(UInt8(self.deactivationIntegrateCounter))
        [bw.write_uint16(UInt16(frame)) for frame in self.deactivationNumInactiveFrames]

        bw.align_to(16)

        self.motionState.serialize(hkFile, bw, obj)

        bw.write_vector(self.inertiaAndMassInv)

        bw.write_vector(self.linearVelocity)
        bw.write_vector(self.angularVelocity)

        [bw.write_vector(drp) for drp in self.deactivationRefPosition]
        bw.write_uint32(UInt32(self.deactivationRefOrientation))

        bw.align_to(8)

        savedMotion_offset = hkFile._write_empty_pointer(bw)

        bw.write_uint16(UInt16(self.savedQualityTypeIndex))

        bw.write_float16(Float16(self.gravityFactor))

    def as_dict(self):
        d = super().as_dict()
        d.update(
            {
                "type": MotionType(self.type).name,
                "deactivationIntegrateCounter": self.deactivationIntegrateCounter,
                "deactivationNumInactiveFrames": self.deactivationNumInactiveFrames,
                "motionState": self.motionState.as_dict(),
                "inertiaAndMassInv": self.inertiaAndMassInv.as_dict(),
                "linearVelocity": self.linearVelocity.as_dict(),
                "angularVelocity": self.angularVelocity.as_dict(),
                "deactivationRefPosition": [
                    pos.as_dict() for pos in self.deactivationRefPosition
                ],
                "deactivationRefOrientation": self.deactivationRefOrientation,
                # "savedMotion": self.savedMotion.as_dict(),
                "savedQualityTypeIndex": self.savedQualityTypeIndex,
                "gravityFactor": self.gravityFactor,
            }
        )
        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().from_dict(d).__dict__)

        inst.type = getattr(MotionType, d["type"]).value
        inst.deactivationIntegrateCounter = d["deactivationIntegrateCounter"]
        inst.deactivationNumInactiveFrames = d["deactivationNumInactiveFrames"]
        inst.motionState = hkMotionState.from_dict(d["motionState"])
        inst.inertiaAndMassInv = Vector4.from_dict(d["inertiaAndMassInv"])
        inst.linearVelocity = Vector4.from_dict(d["linearVelocity"])
        inst.angularVelocity = Vector4.from_dict(d["angularVelocity"])
        inst.deactivationRefPosition = [
            Vector4.from_dict(pos) for pos in d["deactivationRefPosition"]
        ]
        inst.deactivationRefOrientation = d["deactivationRefOrientation"]
        # inst.savedMotion = hkpMaxSizeMotion.from_dict(d["savedMotion"])
        inst.savedQualityTypeIndex = d["savedQualityTypeIndex"]
        inst.gravityFactor = d["gravityFactor"]

        return inst
