from typing import List

from ...binary import BinaryReader, BinaryWriter
from ...util import Vector4
from ..enums.MotionType import MotionType
from .hkMotionState import hkMotionState
from .hkReferencedObject import hkReferencedObject

if False:
    from ...hk import HK
    from .hkpMaxSizeMotion import hkpMaxSizeMotion


class hkpMotion(hkReferencedObject):
    type: int
    deactivationIntegrateCounter: int
    deactivationNumInactiveFrames: List[int]

    motionState: hkMotionState

    inertiaAndMassInv: Vector4

    linearVelocity: Vector4
    angularVelocity: Vector4

    deactivationRefPosition: List[Vector4]
    deactivationRefOrientation: int

    # savedMotion: "hkpMaxSizeMotion" = None
    savedQualityTypeIndex: int

    gravityFactor: float

    def deserialize(self, hk: "HK", br: BinaryReader):
        super().deserialize(hk, br)

        self.type = br.read_uint8()
        self.deactivationIntegrateCounter = br.read_uint8()
        self.deactivationNumInactiveFrames = [br.read_uint16() for _ in range(2)]

        br.align_to(16)  # TODO: Check if this is right

        self.motionState = hkMotionState()
        self.motionState.deserialize(hk, br)

        self.inertiaAndMassInv = br.read_vector4()

        self.linearVelocity = br.read_vector4()
        self.angularVelocity = br.read_vector4()

        self.deactivationRefPosition = [br.read_vector4() for _ in range(2)]
        self.deactivationRefOrientation = br.read_uint32()

        br.align_to(8)  # FIXME: Not sure

        savedMotion_offset = br.tell()
        hk._assert_pointer(br)

        self.savedQualityTypeIndex = br.read_uint16()

        self.gravityFactor = br.read_half()

    def serialize(self, hk: "HK", bw: BinaryWriter):
        super().serialize(hk, bw)

        bw.write_uint8(self.type)
        bw.write_uint8(self.deactivationIntegrateCounter)
        [bw.write_uint16(frame) for frame in self.deactivationNumInactiveFrames]

        bw.align_to(16)

        self.motionState.serialize(hk, bw)

        bw.write_vector4(self.inertiaAndMassInv)

        bw.write_vector4(self.linearVelocity)
        bw.write_vector4(self.angularVelocity)

        [bw.write_vector4(drp) for drp in self.deactivationRefPosition]
        bw.write_uint32(self.deactivationRefOrientation)

        bw.align_to(8)

        savedMotion_offset = bw.tell()
        hk._write_empty_pointer(bw)

        bw.write_uint16(self.savedQualityTypeIndex)

        bw.write_half(self.gravityFactor)

    def asdict(self):
        d = super().asdict()
        d.update(
            {
                "type": MotionType(self.type).name,
                "deactivationIntegrateCounter": self.deactivationIntegrateCounter,
                "deactivationNumInactiveFrames": self.deactivationNumInactiveFrames,
                "motionState": self.motionState.asdict(),
                "inertiaAndMassInv": self.inertiaAndMassInv.asdict(),
                "linearVelocity": self.linearVelocity.asdict(),
                "angularVelocity": self.angularVelocity.asdict(),
                "deactivationRefPosition": [
                    pos.asdict() for pos in self.deactivationRefPosition
                ],
                "deactivationRefOrientation": self.deactivationRefOrientation,
                # "savedMotion": self.savedMotion.asdict(),
                "savedQualityTypeIndex": self.savedQualityTypeIndex,
                "gravityFactor": self.gravityFactor,
            }
        )
        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.type = getattr(MotionType, d["type"]).value
        inst.deactivationIntegrateCounter = d["deactivationIntegrateCounter"]
        inst.deactivationNumInactiveFrames = d["deactivationNumInactiveFrames"]
        inst.motionState = hkMotionState.fromdict(d["motionState"])
        inst.inertiaAndMassInv = Vector4.fromdict(d["inertiaAndMassInv"])
        inst.linearVelocity = Vector4.fromdict(d["linearVelocity"])
        inst.angularVelocity = Vector4.fromdict(d["angularVelocity"])
        inst.deactivationRefPosition = [
            Vector4.fromdict(pos) for pos in d["deactivationRefPosition"]
        ]
        inst.deactivationRefOrientation = d["deactivationRefOrientation"]
        # inst.savedMotion = hkpMaxSizeMotion.fromdict(d["savedMotion"])
        inst.savedQualityTypeIndex = d["savedQualityTypeIndex"]
        inst.gravityFactor = d["gravityFactor"]

        return inst
