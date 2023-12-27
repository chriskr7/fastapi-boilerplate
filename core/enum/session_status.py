from enum import Enum, auto, unique


@unique
class SessionStatus(Enum):
    NORMAL = 0
    NOT_EXIST = auto()
    EXPIRED = auto()
