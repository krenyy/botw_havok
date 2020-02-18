from ...binary import BinaryReader, BinaryWriter
from ..enums.MotionType import MotionType
from .hkReferencedObject import hkReferencedObject
from ...util import Vector4
from .hkMotionState import hkMotionState

if False:
    from ...hk import HK
    from .hkpMaxSizeMotion import hkpMaxSizeMotion


class hkpMotion(hkReferencedObject):
    type: int
    deactivationIntegrateCounter: int
    deactivationNumInactiveFrames: int

    motionState: hkMotionState

    inertiaAndMassInv: Vector4

    linearVelocity: Vector4
    angularVelocity: Vector4

    deactivationRefPosition: Vector4
    deactivationRefOrientation: int

    savedMotion: "hkpMaxSizeMotion" = None
    savedQualityTypeIndex: int

    gravityFactor: float

    def deserialize(self, hk: "HK", br: BinaryReader):
        super().deserialize(hk, br)

        self.type = br.read_uint8()
        self.deactivationIntegrateCounter = br.read_uint8()
        self.deactivationNumInactiveFrames = br.read_uint16()

        self.motionState.deserialize(hk, br)

        self.inertiaAndMassInv = br.read_vector4()

        self.linearVelocity = br.read_vector4()
        self.angularVelocity = br.read_vector4()

        self.deactivationRefPosition = br.read_vector4()
        self.deactivationRefOrientation = br.read_uint32()

        savedMotion_offset = br.tell()
        hk._assert_pointer(br)

        self.savedQualityTypeIndex = br.read_uint16()

        self.gravityFactor = br.read_half()

    def serialize(self, hk: "HK", bw: BinaryWriter):
        super().serialize(hk, bw)

        bw.write_uint8(self.type)
        bw.write_uint8(self.deactivationIntegrateCounter)
        bw.write_uint16(self.deactivationNumInactiveFrames)

        self.motionState.serialize(hk, bw)

        bw.write_vector4(self.inertiaAndMassInv)

        bw.write_vector4(self.linearVelocity)
        bw.write_vector4(self.angularVelocity)

        bw.write_vector4(self.deactivationRefPosition)
        bw.write_uint32(self.deactivationRefOrientation)

        savedMotion_offset = bw.tell()
        hk._write_empty_pointer()

        bw.write_uint16(self.savedQualityTypeIndex)

        bw.write_half(self.gravityFactor)

    def asdict(self):
        d = super().asdict()
        d.update(
            {
                "type": MotionType(self.type).name,
                "deactivationIntegrateCounter": self.deactivationIntegrateCounter,
                "deactivationNumInactiveFrames": self.deactivationNumInactiveFrames,
                "motionState": self.motionState,
                "inertiaAndMassInv": self.inertiaAndMassInv,
                "linearVelocity": self.linearVelocity,
                "angularVelocity": self.angularVelocity,
                "deactivationRefPosition": self.deactivationRefPosition,
                "deactivationRefOrientation": self.deactivationRefOrientation,
                "savedMotion": self.savedMotion,
                "savedQualityTypeIndex": self.savedQualityTypeIndex,
                "gravityFactor": self.gravityFactor,
            }
        )
        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.memSizeAndRefCount = d["memSizeAndRefCount"]
        inst.type = getattr(MotionType, d["type"]).value
        inst.deactivationIntegrateCounter = d["deactivationIntegrateCounter"]
        inst.deactivationNumInactiveFrames = d["deactivationNumInactiveFrames"]
        inst.motionState = d["motionState"]
        inst.inertiaAndMassInv = d["inertiaAndMassInv"]
        inst.linearVelocity = d["linearVelocity"]
        inst.angularVelocity = d["angularVelocity"]
        inst.deactivationRefPosition = d["deactivationRefPosition"]
        inst.deactivationRefOrientation = d["deactivationRefPosition"]
        inst.savedMotion = d["savedMotion"]
        inst.savedQualityTypeIndex = d["savedQualityTypeIndex"]
        inst.gravityFactor = d["gravityFactor"]
