class hkcdStaticMeshTreeBaseSectionSharedVertices:
    data: int

    def deserialize(self, hk, br, obj):
        self.data = br.read_uint32()

    def serialize(self, hk, bw, obj):
        bw.write_uint32(self.data)

    def asdict(self):
        return {"data": self.data}

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()

        inst.data = d["data"]

        return inst
