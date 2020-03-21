from typing import List


class hkcdStaticMeshTreeBasePrimitive:
    indices: List[int]

    def deserialize(self, hk, br, obj):
        self.indices = [br.read_uint8() for _ in range(4)]

    def serialize(self, hk, bw, obj):
        [bw.write_uint8(i) for i in self.indices]

    def asdict(self):
        return {"indices": self.indices}

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()

        inst.indices = d["indices"]

        return inst
