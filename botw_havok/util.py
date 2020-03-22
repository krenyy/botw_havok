from typing import List


class Vector3:
    x: int
    y: int
    z: int

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, value: "Vector3"):
        if isinstance(value, Vector3):
            return (self.x == value.x) and (self.y == value.y) and (self.z == value.z)
        return False

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def asdict(self):
        return [self.x, self.y, self.z]

    @classmethod
    def fromdict(cls, d: list):
        return cls(d[0], d[1], d[2])


class Vector4(Vector3):
    w: int

    def __init__(self, x=None, y=None, z=None, w=None, v3: Vector3 = None):
        if isinstance(v3, Vector3):
            self.x = v3.x
            self.y = v3.y
            self.z = v3.z
        else:
            super().__init__(x, y, z)
        self.w = w

    def __eq__(self, value: "Vector4"):
        if isinstance(value, Vector4):
            return super().__eq__(value) and (self.w == value.w)
        return False

    def __iter__(self):
        return iter((self.x, self.y, self.z, self.w))

    def asdict(self):
        return [self.x, self.y, self.z, self.w]

    @classmethod
    def fromdict(cls, d: list):
        return cls(d[0], d[1], d[2], d[3])

    def __repr__(self):
        return f"Vector4({self.x}, {self.y}, {self.z}, {self.w})"


class Matrix:
    _matrix: List[Vector4]

    def __init__(self, matrix):
        self._matrix = matrix

    def asdict(self):
        return [v4.asdict() for v4 in self._matrix]

    @classmethod
    def fromdict(cls, d: list):
        return cls(d)

    def __len__(self):
        return len(self._matrix)

    def __getitem__(self, idx: int):
        return self._matrix[idx]

    def __iter__(self):
        return iter((self._matrix))

    def __repr__(self):
        return f"{self.__class__.__name__}({self._matrix})"
