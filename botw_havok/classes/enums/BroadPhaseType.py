from enum import Enum


class BroadPhaseType(Enum):
    BROAD_PHASE_INVALID = 0
    BROAD_PHASE_ENTITY = 1
    BROAD_PHASE_PHANTOM = 2
    BROAD_PHASE_BORDER = 3
    BROAD_PHASE_MAX_ID = 4
