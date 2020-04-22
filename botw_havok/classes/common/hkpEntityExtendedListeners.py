from .hkpEntitySmallArraySerializeOverrideType import (
    hkpEntitySmallArraySerializeOverrideType,
)


class hkpEntityExtendedListeners:
    activationListeners: hkpEntitySmallArraySerializeOverrideType
    entityListeners: hkpEntitySmallArraySerializeOverrideType

    def deserialize(self, hkFile, br):
        self.activationListeners = hkpEntitySmallArraySerializeOverrideType()
        self.activationListeners.deserialize(hkFile, br)

        self.entityListeners = hkpEntitySmallArraySerializeOverrideType()
        self.entityListeners.deserialize(hkFile, br)

    def serialize(self, hkFile, bw):
        self.activationListeners.serialize(hkFile, bw)
        self.entityListeners.serialize(hkFile, bw)

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
