from ...binary import BinaryReader, BinaryWriter

if False:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkObject:
    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        raise NotImplementedError("This method is meant to be overridden!")

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        raise NotImplementedError("This method is meant to be overridden!")

    def __eq__(self, value: object):
        if not isinstance(value, hkObject):
            raise NotImplementedError()
        comparison = self.__dict__ == value.__dict__
        if not comparison:
            print(f"Subclass '{self.__class__.__name__}' doesn't match")
            print("\n****")
            print(self.__dict__)
            print("****")
            print(value.__dict__)
            print("****\n")
        return comparison
