from typing import List, Optional

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


class Vector3(List[Float32]):
    def __init__(self, x: Optional[Float32] = None, y: Optional[Float32] = None, z: Optional[Float32] = None):
        super().__init__([x or Float32(0.0), y or Float32(0.0), z or Float32(0.0)])

    def as_dict(self):
        return self

    @classmethod
    def from_dict(cls, l: list):
        return cls(*[Float32(f) for f in l])

    def __sub__(self, other):
        if not isinstance(other, self.__class__) or not len(self) == len(other):
            raise NotImplementedError()

        return self.__class__(*[f1 - f2 for f1, f2 in zip(self, other)])

    def __repr__(self):
        return f"{self.__class__.__name__}{tuple(self)}"


class Vector4(List[Float32]):
    def __init__(self, x: Optional[Float32] = None, y: Optional[Float32] = None, z: Optional[Float32] = None,
                 w: Optional[Float32] = None):
        super().__init__([x or Float32(0.0), y or Float32(0.0), z or Float32(0.0), w or Float32(0.0)])

    def as_dict(self):
        return self

    @classmethod
    def from_dict(cls, l: list):
        return cls(*[Float32(f) for f in l])

    def __sub__(self, other):
        if not isinstance(other, self.__class__) or not len(self) == len(other):
            raise NotImplementedError()

        return self.__class__(*[f1 - f2 for f1, f2 in zip(self, other)])

    def __repr__(self):
        return f"{self.__class__.__name__}{tuple(self)}"


class Matrix(List[Vector4]):
    def __init__(self, *args):
        super().__init__()
        self.extend(args)

    def as_dict(self):
        return [v.as_dict() for v in self]

    @classmethod
    def from_dict(cls, l: list):
        return cls(*[Vector4.from_dict(v) for v in l])

    def __repr__(self):
        return f"{self.__class__.__name__}{tuple(self)}"
