from typing import TYPE_CHECKING

from .hkObject import hkObject
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Int16, Int32, UInt16

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class ShapeInfo(hkObject):
    ActorInfoIndex: Int32
    InstanceId: Int32
    BodyGroup: Int16
    BodyLayerType: UInt16

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        self.ActorInfoIndex = br.read_int32()
        self.InstanceId = br.read_int32()
        self.BodyGroup = br.read_int16()
        self.BodyLayerType = br.read_uint16()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        bw.write_int32(self.ActorInfoIndex)
        bw.write_int32(self.InstanceId)
        bw.write_int16(self.BodyGroup)
        bw.write_uint16(self.BodyLayerType)

    def as_dict(self):
        return {
            "ActorInfoIndex": self.ActorInfoIndex,
            "InstanceId": self.InstanceId,
            "BodyGroup": self.BodyGroup,
            "BodyLayerType": self.BodyLayerType,
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.ActorInfoIndex = Int32(d["ActorInfoIndex"])
        inst.InstanceId = Int32(d["InstanceId"])
        inst.BodyGroup = Int16(d["BodyGroup"])
        inst.BodyLayerType = UInt16(d["BodyLayerType"])

        return inst

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.ActorInfoIndex}, "
            f"{self.InstanceId}, {self.BodyGroup}, {self.BodyLayerType})"
        )
