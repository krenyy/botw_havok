# https://stackoverflow.com/questions/1036409/recursively-convert-python-object-graph-to-dictionary
def todict(obj, classkey=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data
    elif hasattr(obj, "asdict"):
        return todict(obj.asdict())
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict(
            [
                (key, todict(value, classkey))
                for key, value in obj.__dict__.items()
                if not callable(value) and not key.startswith("_")
            ]
        )
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj


class Vector3:
    x: int
    y: int
    z: int

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, value: "Vector4"):
        if isinstance(value, Vector4):
            return (self.x == value.x) and (self.y == value.y) and (self.z == value.z)
        return False

    def __iter__(self):
        return iter((self.x, self.y, self.z))


class Vector4(Vector3):
    w: int

    def __init__(self, x, y, z, w):
        super().__init__(x, y, z)
        self.w = w

    def __eq__(self, value: "Vector4"):
        if isinstance(value, Vector4):
            return (
                (self.x == value.x)
                and (self.y == value.y)
                and (self.z == value.z)
                and (self.w == value.w)
            )

    def __iter__(self):
        return iter((self.x, self.y, self.z, self.w))
