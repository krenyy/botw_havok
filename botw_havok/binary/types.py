"""
TYPES

"""

from typing import Any, List


class BinaryType:
    pass


class BaseNum(BinaryType):
    def __init__(self, *args):
        if isinstance(self, BaseFloat):
            if float("+inf") > self.real > self.max_value:
                self.real = type(self)("+inf")
            elif float("-inf") < self < self.min_value:
                self.real = type(self)("-inf")

        elif not (self.min_value <= self.real <= self.max_value):
            raise TypeError(f"Invalid range for type {self.__class__.__name__}")

    def __eq__(self, value: object):
        if (
            not isinstance(value, self.__class__)
            and not isinstance(value, float)
            and not isinstance(value, int)
        ):
            raise NotImplementedError()
        return self.real == value.real

    def __gt__(self, value: object):
        if (
            not isinstance(value, self.__class__)
            and not isinstance(value, float)
            and not isinstance(value, int)
        ):
            raise NotImplementedError()
        return self.real > value.real

    def __add__(self, value: object):
        if (
            not isinstance(value, self.__class__)
            and not isinstance(value, float)
            and not isinstance(value, int)
        ):
            raise NotImplementedError()
        return self.__class__(self.real + value.real)

    def __sub__(self, value: object):
        if (
            not isinstance(value, self.__class__)
            and not isinstance(value, float)
            and not isinstance(value, int)
        ):
            raise NotImplementedError()
        return self.__class__(self.real - value.real)

    def __mul__(self, value: object):
        if (
            not isinstance(value, self.__class__)
            and not isinstance(value, float)
            and not isinstance(value, int)
        ):
            raise NotImplementedError()
        return self.__class__(self.real * value.real)

    def __div__(self, value: object):
        if (
            not isinstance(value, self.__class__)
            and not isinstance(value, float)
            and not isinstance(value, int)
        ):
            raise NotImplementedError()
        return self.__class__(self.real / value.real)

    def __repr__(self):
        return f"{self.real}"


class BaseInt(BaseNum, int):
    real: int = 0

    def __init__(self, *args):
        self.real = int(*args)

        super().__init__()


class BaseFloat(BaseNum, float):
    real: float = 0.0

    def __init__(self, *args):
        self.real = float(*args)

        super().__init__()


class Int8(BaseInt):
    min_value: int = -128
    max_value: int = 127


class Int16(BaseInt):
    min_value: int = -32768
    max_value: int = 32767


class Int32(BaseInt):
    min_value: int = -2_147_483_648
    max_value: int = 2_147_483_647


class Int64(BaseInt):
    min_value: int = -9_223_372_036_854_775_808
    max_value: int = 9_223_372_036_854_775_807


class UInt8(BaseInt):
    min_value: int = 0
    max_value: int = 255


class UInt16(BaseInt):
    min_value: int = 0
    max_value: int = 65535


class UInt32(BaseInt):
    min_value: int = 0
    max_value: int = 4_294_967_295


class UInt64(BaseInt):
    min_value: int = 0
    max_value: int = 18_446_744_073_709_551_615


class Float16(BaseFloat):
    min_value: float = -65520
    max_value: float = +65520


class Float32(BaseFloat):
    min_value: float = -3.402820018375656e38
    max_value: float = +3.402820018375656e38


class Float64(BaseFloat):
    min_value: float = -1.7e308
    max_value: float = +1.7e308


class Bool(BinaryType):
    real: int

    def __init__(self, x: Any = None):
        if not x:
            self.real = 0
        else:
            self.real = int(bool(x))

    def __int__(self):
        return self.real

    def __eq__(self, value: object):
        if not isinstance(value, Bool):
            raise NotImplementedError()
        return self.real == value.real

    def __gt__(self, value: object):
        if not isinstance(value, Bool):
            raise NotImplementedError()
        return self.real > value.real

    def __repr__(self):
        return f"{bool(self.real)}"


class String(str, BinaryType):
    pass


class Vector3(List[Float32], BinaryType):
    def __init__(self, *args):
        if not args:
            super().__init__([Float32(0.0) for _ in range(3)])
        elif len(args) == 3:
            super().__init__([Float32(f) for f in args])
        else:
            raise NotImplementedError()

    def asdict(self):
        return self

    @classmethod
    def fromdict(cls, items: list):
        return cls(*[Float32(i) for i in items])


class Vector4(List[Float32], BinaryType):
    def __init__(self, *args):
        if not args:
            super().__init__([Float32(0.0) for _ in range(4)])
            self.append(Float32(0.0))
        elif len(args) == 4:
            super().__init__([Float32(f) for f in args])
        else:
            raise NotImplementedError()

    def asdict(self):
        return self

    @classmethod
    def fromdict(cls, items: list):
        return cls(*[Float32(i) for i in items])


class Matrix(List[Vector4], BinaryType):
    def __init__(self, *args):
        if not args:
            self.extend([Vector4(*[0.0] * 4) for _ in range(4)])
        else:
            self.extend(args)

    def asdict(self):
        return [v.asdict() for v in self]

    @classmethod
    def fromdict(cls, matrix: list):
        return cls(*[Vector4.fromdict(v) for v in matrix])

    def __repr__(self):
        return f"{self.__class__.__name__}{tuple(self)}"
