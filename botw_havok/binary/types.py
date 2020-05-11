from typing import List

import numpy as _np

Float16 = _np.float16
Float32 = _np.float32
Float64 = _np.float64
Int8 = _np.int8
Int16 = _np.int16
Int32 = _np.int32
Int64 = _np.int64
UInt8 = _np.uint8
UInt16 = _np.uint16
UInt32 = _np.uint32
UInt64 = _np.uint64


class Vector(List[_np.float32]):
    def __init__(self, *args):
        super().__init__([Float32(f) for f in args])

    def as_dict(self):
        return self

    @classmethod
    def from_dict(cls, l: list):
        return cls(*[Float32(f) for f in l])

    def __repr__(self):
        return f"{self.__class__.__name__}{tuple(self)}"

    def __hash__(self):
        return hash(tuple(self))


class Vector3(Vector):
    pass


class Vector4(Vector):
    pass


class Matrix(List[Vector4]):
    def __init__(self, *args):
        self.extend(args)

    def as_dict(self):
        return [v.as_dict() for v in self]

    @classmethod
    def from_dict(cls, l: list):
        return cls(*[Vector4.from_dict(v) for v in l])

    def __repr__(self):
        return f"{self.__class__.__name__}{tuple(self)}"

    def __hash__(self):
        return hash(tuple(self))
