from .hkpEntitySmallArraySerializeOverrideType import (
    hkpEntitySmallArraySerializeOverrideType,
)


class hkpEntityExtendedListeners:
    activationListeners: hkpEntitySmallArraySerializeOverrideType
    entityListeners: hkpEntitySmallArraySerializeOverrideType

    def deserialize(self, hk, br):
        self.activationListeners = hkpEntitySmallArraySerializeOverrideType()
        self.activationListeners.deserialize(hk, br)

        self.entityListeners = hkpEntitySmallArraySerializeOverrideType()
        self.entityListeners.deserialize(hk, br)

    def serialize(self, hk, bw):
        self.activationListeners.serialize(hk, bw)
        self.entityListeners.serialize(hk, bw)

    def asdict(self):
        return {
            "activationListeners": self.activationListeners.asdict(),
            "entityListeners": self.entityListeners.asdict(),
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.activationListeners = hkpEntitySmallArraySerializeOverrideType.fromdict(
            d["activationListeners"]
        )
        inst.entityListeners = hkpEntitySmallArraySerializeOverrideType.fromdict(
            d["entityListeners"]
        )
        return inst
