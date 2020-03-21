from .hkcdStaticTreeCodec3Axis import hkcdStaticTreeCodec3Axis


class hkcdStaticTreeCodec3Axis5(hkcdStaticTreeCodec3Axis):
    hiData: int
    loData: int

    def deserialize(self, hk, br, obj):
        super().deserialize(hk, br, obj)

        self.hiData = br.read_uint8()
        self.loData = br.read_uint8()

    def serialize(self, hk, bw, obj):
        super().serialize(hk, bw, obj)

        bw.write_uint8(self.hiData)
        bw.write_uint8(self.loData)

    def asdict(self):
        d = super().asdict()
        d.update({"hiData": self.hiData, "loData": self.loData})
        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.hiData = d["hiData"]
        inst.loData = d["loData"]

        return inst
