from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Float16, Float32, Matrix, UInt8, Vector4
from .hkUFloat8 import hkUFloat8


class hkMotionState:
    transform: Matrix
    sweptTransform: Matrix

    deltaAngle: Vector4

    objectRadius: Float32

    linearDamping: Float16
    angularDamping: Float16
    timeFactor: Float16

    maxLinearVelocity: hkUFloat8
    maxAngularVelocity: hkUFloat8

    deactivationClass: UInt8

    def deserialize(self, hkFile, br: BinaryReader):
        self.transform = br.read_matrix(4)
        self.sweptTransform = br.read_matrix(5)

        self.deltaAngle = br.read_vector4()

        self.objectRadius = br.read_float32()

        self.linearDamping = br.read_float16()
        self.angularDamping = br.read_float16()
        self.timeFactor = br.read_float16()

        self.maxLinearVelocity = hkUFloat8()
        self.maxLinearVelocity.deserialize(br)

        self.maxAngularVelocity = hkUFloat8()
        self.maxAngularVelocity.deserialize(br)

        self.deactivationClass = br.read_uint8()

        br.align_to(16)

    def serialize(self, hkFile, bw: BinaryWriter):
        bw.write_matrix(self.transform)
        bw.write_matrix(self.sweptTransform)

        bw.write_vector4(self.deltaAngle)

        bw.write_float32(self.objectRadius)

        bw.write_float16(self.linearDamping)
        bw.write_float16(self.angularDamping)
        bw.write_float16(self.timeFactor)

        self.maxLinearVelocity.serialize(bw)
        self.maxAngularVelocity.serialize(bw)

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
            "maxLinearVelocity": self.maxLinearVelocity.asdict(),
            "maxAngularVelocity": self.maxAngularVelocity.asdict(),
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
        inst.maxLinearVelocity = hkUFloat8.fromdict(d["maxLinearVelocity"])
        inst.maxAngularVelocity = hkUFloat8.fromdict(d["maxAngularVelocity"])
        inst.deactivationClass = d["deactivationClass"]

        return inst
