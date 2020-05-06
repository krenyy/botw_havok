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

    def as_dict(self):
        return {
            "activationListeners": self.activationListeners.as_dict(),
            "entityListeners": self.entityListeners.as_dict(),
        }

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.activationListeners = hkpEntitySmallArraySerializeOverrideType.from_dict(
            d["activationListeners"]
        )
        inst.entityListeners = hkpEntitySmallArraySerializeOverrideType.from_dict(
            d["entityListeners"]
        )
        return inst
