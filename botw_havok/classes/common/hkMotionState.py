from typing import List

from ...binary import BinaryReader, BinaryWriter
from ...util import Transform, Vector4
from .hkUFloat8 import hkUFloat8


class hkMotionState:
    transform: Transform

    sweptTransform: List[Vector4]

    deltaAngle: Vector4

    objectRadius: float

    linearDamping: float
    angularDamping: float

    timeFactor: float

    maxLinearVelocity: hkUFloat8
    maxAngularVelocity: hkUFloat8

    deactivationClass: int

    def deserialize(self, hk, br: BinaryReader):
        self.transform = br.read_transform()

        self.sweptTransform = [br.read_vector4() for _ in range(5)]
        self.deltaAngle = br.read_vector4()

        self.objectRadius = br.read_single()

        self.linearDamping = br.read_half()
        self.angularDamping = br.read_half()

        self.timeFactor = br.read_half()

        # ----

        self.maxLinearVelocity = hkUFloat8()
        self.maxLinearVelocity.deserialize(hk, br)

        self.maxAngularVelocity = hkUFloat8()
        self.maxAngularVelocity.deserialize(hk, br)

        # ----

        self.deactivationClass = br.read_uint8()

        br.align_to(16)  # FIXME: Is this right?

    def serialize(self, hk, bw: BinaryWriter):
        bw.write_transform(self.transform)

        [bw.write_vector4(st) for st in self.sweptTransform]
        bw.write_vector4(self.deltaAngle)

        bw.write_single(self.objectRadius)

        bw.write_half(self.linearDamping)
        bw.write_half(self.angularDamping)

        bw.write_half(self.timeFactor)

        # ----

        self.maxLinearVelocity.serialize(hk, bw)
        self.maxAngularVelocity.serialize(hk, bw)

        # ----

        bw.write_uint8(self.deactivationClass)

        bw.align_to(16)

    def asdict(self):
        return {
            "transform": self.transform.asdict(),
            "sweptTransform": [st.asdict() for st in self.sweptTransform],
            "deltaAngle": self.deltaAngle.asdict(),
            "objectRadius": self.objectRadius,
            "linearDamping": self.linearDamping,
            "angularDamping": self.angularDamping,
            "timeFactor": self.timeFactor,
            "maxLinearVelocity": self.maxLinearVelocity.asdict(),
            "maxAngularVelocity": self.maxAngularVelocity.asdict(),
            "deactivationClass": self.deactivationClass,
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.transform = Transform.fromdict(d["transform"])
        inst.sweptTransform = [Vector4.fromdict(st) for st in d["sweptTransform"]]
        inst.deltaAngle = Vector4.fromdict(d["deltaAngle"])
        inst.objectRadius = d["objectRadius"]
        inst.linearDamping = d["linearDamping"]
        inst.angularDamping = d["angularDamping"]
        inst.timeFactor = d["timeFactor"]
        inst.maxLinearVelocity = hkUFloat8.fromdict(d["maxLinearVelocity"])
        inst.maxAngularVelocity = hkUFloat8.fromdict(d["maxAngularVelocity"])
        inst.deactivationClass = d["deactivationClass"]

        return inst
