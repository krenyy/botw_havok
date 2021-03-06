from enum import Enum


class EdgeFlagBits(Enum):
    EDGE_SILHOUETTE = 1
    EDGE_RETRIANGULATED = 2
    EDGE_ORIGINAL = 4
    OPPOSITE_EDGE_UNLOADED_UNUSED = 8
    EDGE_USER = 16
    EDGE_BLOCKED = 32
    EDGE_EXTERNAL_OPPOSITE = 64
