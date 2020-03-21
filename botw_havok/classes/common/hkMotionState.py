from typing import List

from ...binary import BinaryReader, BinaryWriter
from ...util import Matrix, Vector4


class hkMotionState:
    transform: Matrix
    sweptTransform: Matrix

    deltaAngle: Vector4

    objectRadius: float

    linearDamping: float
    angularDamping: float
    timeFactor: float

    maxLinearVelocity: float
    maxAngularVelocity: float

    deactivationClass: int

    def deserialize(self, hk, br: BinaryReader):
        self.transform = br.read_matrix(4)
        self.sweptTransform = br.read_matrix(5)

        self.deltaAngle = br.read_vector4()

        self.objectRadius = br.read_single()

        self.linearDamping = br.read_half()
        self.angularDamping = br.read_half()
        self.timeFactor = br.read_half()

        self.maxLinearVelocity = br.read_floatu8()
        self.maxAngularVelocity = br.read_floatu8()

        self.deactivationClass = br.read_uint8()

        br.align_to(16)

    def serialize(self, hk, bw: BinaryWriter):
        bw.write_matrix(self.transform)
        bw.write_matrix(self.sweptTransform)

        bw.write_vector4(self.deltaAngle)

        bw.write_single(self.objectRadius)

        bw.write_half(self.linearDamping)
        bw.write_half(self.angularDamping)
        bw.write_half(self.timeFactor)

        bw.write_floatu8(self.maxLinearVelocity)
        bw.write_floatu8(self.maxAngularVelocity)

        bw.write_uint8(self.deactivationClass)

        bw.align_to(16)

    def asdict(self):
        return {
            "transform": self.transform.asdict(),
            "sweptTransform": self.sweptTransform.asdict(),
            "deltaAngle": self.deltaAngle.asdict(),
            "objectRadius": self.objectRadius,
            "linearDamping": self.linearDamping,
            "angularDamping": self.angularDamping,
            "timeFactor": self.timeFactor,
            "maxLinearVelocity": self.maxLinearVelocity,
            "maxAngularVelocity": self.maxAngularVelocity,
            "deactivationClass": self.deactivationClass,
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.transform = Matrix.fromdict(d["transform"])
        inst.sweptTransform = Matrix.fromdict(d["sweptTransform"])
        inst.deltaAngle = Vector4.fromdict(d["deltaAngle"])
        inst.objectRadius = d["objectRadius"]
        inst.linearDamping = d["linearDamping"]
        inst.angularDamping = d["angularDamping"]
        inst.timeFactor = d["timeFactor"]
        inst.maxLinearVelocity = d["maxLinearVelocity"]
        inst.maxAngularVelocity = d["maxAngularVelocity"]
        inst.deactivationClass = d["deactivationClass"]

        return inst
