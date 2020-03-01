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


class Matrix3:
    _matrix3: List[Vector4]

    def __init__(self, matrix):
        if len(matrix) == 3:
            self._matrix3 = matrix
        else:
            raise Exception("Matrix3 only accepts lists of length 3")

    def __iter__(self):
        return iter((self._matrix3))

    def asdict(self):
        return [v4.asdict() for v4 in self._matrix3]

    @classmethod
    def fromdict(cls, d: list):
        return cls(d)

    def __repr__(self):
        return f"Matrix3({self._matrix3})"


class QsTransform:
    translation: Vector4
    rotation: Vector4
    scale: Vector4

    def __init__(self, matrix):
        self.translation = matrix[0]
        self.rotation = matrix[1]
        self.scale = matrix[2]

    def __iter__(self):
        return iter((self.translation, self.rotation, self.scale))

    def asdict(self):
        return {
            "translation": self.translation.asdict(),
            "rotation": self.rotation.asdict(),
            "scale": self.scale.asdict(),
        }

    @classmethod
    def fromdict(cls, d: dict):
        return cls(
            [
                Vector4.fromdict(d["translation"]),
                Vector4.fromdict(d["rotation"]),
                Vector4.fromdict(d["scale"]),
            ]
        )


class Transform(QsTransform):
    shear: Vector4

    def __init__(self, matrix):
        super().__init__(matrix)

        self.shear = matrix[3]

    def __eq__(self, value: "Transform"):
        if isinstance(value, Transform):
            return (
                (self.translation == value.translation)
                and (self.rotation == value.rotation)
                and (self.scale == value.scale)
                and (self.shear == value.shear)
            )
        return False

    def __iter__(self):
        return iter((self.translation, self.rotation, self.scale, self.shear))

    def asdict(self):
        d = super().asdict()
        d.update(
            {"shear": self.shear.asdict(),}
        )

        return d

    @classmethod
    def fromdict(cls, d: dict):
        return cls(
            [
                Vector4.fromdict(d["translation"]),
                Vector4.fromdict(d["rotation"]),
                Vector4.fromdict(d["scale"]),
                Vector4.fromdict(d["shear"]),
            ]
        )
