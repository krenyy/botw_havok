from typing import List
from botw_havok.binary.types import Vector3


class WaveformVertex:
    vec: Vector3

    def __init__(self, vec: Vector3):
        self.vec = vec

    def as_waveform(self):
        return f"v {' '.join([str(f) for f in self.vec])}"


class WaveformFace:
    indices: List[int]

    def __init__(self, indices: List[int] = None):
        self.indices = indices or []

    def as_waveform(self):
        return f"f {' '.join([str(idx) for idx in self.indices])}"

    def get_max_index(self):
        return max(self.indices)

    def increase_index(self, value: int):
        self.indices = [index + value for index in self.indices]

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([str(idx) for idx in self.indices])})"


class WaveformObject:
    name: str
    vertices: List[WaveformVertex]
    faces: List[WaveformFace]

    def __init__(
        self,
        name: str,
        vertices: List[WaveformVertex] = None,
        faces: List[WaveformFace] = None,
    ):
        self.name = name
        self.vertices = vertices or []
        self.faces = faces or []

    def as_waveform(self):
        return "\n".join([
            f"o {self.name}",
            *[vertex.as_waveform() for vertex in self.vertices],
            *[face.as_waveform() for face in self.faces],
        ])

    def get_max_index(self):
        return len(self.vertices)

    def increase_index(self, value: int):
        [face.increase_index(value) for face in self.faces]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {len(self.vertices)}, {len(self.faces)})"


def parse_obj(args):
    objects = []

    with open(args.objFile, 'r') as f:
        for line in f.readlines():
            if line.startswith('o '):
                objects.append(WaveformObject(name=line[2:].rstrip('\n')))
            elif line.startswith('v '):
                objects[-1].vertices.append(
                    WaveformVertex(
                        *[
                            float(f) for f in line.split()[1:]
                        ]
                    )
                )
            elif line.startswith('f '):
                objects[-1].faces.append(
                    WaveformFace(
                        *[
                            float(f) for f in line.split()[1:]
                        ]
                    )
                )
            else:
                raise NotImplementedError()

    return objects
