from ...binary import BinaryReader, BinaryWriter
from .hkSimplePropertyValue import hkSimplePropertyValue


if False:
    from ...hk import HK


class hkSimpleProperty:
    key: int
    value: hkSimplePropertyValue

    def deserialize(self, hk: "HK", br: BinaryReader):
        self.key = br.read_uint32()

        if hk.header.padding_option:
            br.read_uint32()

        self.value = hkSimplePropertyValue()
        self.value.deserialize(hk, br)

    def serialize(self, hk: "HK", bw: BinaryWriter):
        bw.write_uint32(self.key)

        if hk.header.padding_option:
            bw.write_uint32()

        self.value.serialize(hk, bw)

    def asdict(self):
        return {"key": self.key, "value": self.value.asdict()}

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.key = d["key"]
        inst.value = hkSimplePropertyValue.fromdict(d["value"])

        return inst
