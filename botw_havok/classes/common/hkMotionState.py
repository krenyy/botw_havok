from typing import TYPE_CHECKING

from .hkObject import hkObject
from .hkUFloat8 import hkUFloat8
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Float16, Float32, Matrix, UInt8, Vector4

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkMotionState(hkObject):
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

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.transform = br.read_matrix(4)
        self.sweptTransform = br.read_matrix(5)

        self.deltaAngle = br.read_vector4()

        self.objectRadius = br.read_float32()

        self.linearDamping = br.read_float16()
        self.angularDamping = br.read_float16()
        self.timeFactor = br.read_float16()

        self.maxLinearVelocity = hkUFloat8()
        self.maxLinearVelocity.deserialize(hkFile, br, obj)

        self.maxAngularVelocity = hkUFloat8()
        self.maxAngularVelocity.deserialize(hkFile, br, obj)

        self.deactivationClass = br.read_uint8()

        br.align_to(16)

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_matrix(self.transform)
        bw.write_matrix(self.sweptTransform)

        bw.write_vector(self.deltaAngle)

        bw.write_float32(self.objectRadius)

        bw.write_float16(self.linearDamping)
        bw.write_float16(self.angularDamping)
        bw.write_float16(self.timeFactor)

        self.maxLinearVelocity.serialize(hkFile, bw, obj)
        self.maxAngularVelocity.serialize(hkFile, bw, obj)

        bw.write_uint8(self.deactivationClass)

        bw.align_to(16)

    def as_dict(self):
        return {
            "transform": self.transform.as_dict(),
            "sweptTransform": self.sweptTransform.as_dict(),
            "deltaAngle": self.deltaAngle.as_dict(),
            "objectRadius": self.objectRadius,
            "linearDamping": self.linearDamping,
            "angularDamping": self.angularDamping,
            "timeFactor": self.timeFactor,
            "maxLinearVelocity": self.maxLinearVelocity.as_dict(),
            "maxAngularVelocity": self.maxAngularVelocity.as_dict(),
            "deactivationClass": self.deactivationClass,
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.transform = Matrix.from_dict(d["transform"])
        inst.sweptTransform = Matrix.from_dict(d["sweptTransform"])
        inst.deltaAngle = Vector4.from_dict(d["deltaAngle"])
        inst.objectRadius = d["objectRadius"]
        inst.linearDamping = d["linearDamping"]
        inst.angularDamping = d["angularDamping"]
        inst.timeFactor = d["timeFactor"]
        inst.maxLinearVelocity = hkUFloat8.from_dict(d["maxLinearVelocity"])
        inst.maxAngularVelocity = hkUFloat8.from_dict(d["maxAngularVelocity"])
        inst.deactivationClass = d["deactivationClass"]

        return inst
