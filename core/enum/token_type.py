from enum import Enum, auto, unique


@unique
class TokenType(Enum):
    ACCESS = 0
    REFRESH = auto()
