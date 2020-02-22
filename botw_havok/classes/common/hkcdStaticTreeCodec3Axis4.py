from .hkcdStaticTreeCodec3Axis import hkcdStaticTreeCodec3Axis


class hkcdStaticTreeCodec3Axis4(hkcdStaticTreeCodec3Axis):
    data: int

    def deserialize(self, hk, br, obj):
        super().deserialize(hk, br, obj)

        self.data = br.read_uint8()

    def serialize(self, hk, bw, obj):
        super().serialize(hk, bw, obj)

        bw.write_uint8(self.data)

    def asdict(self):
        d = super().asdict()
        d.update({"data": self.data})
        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.data = d["data"]

        return inst
