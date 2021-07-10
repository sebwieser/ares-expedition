from enum import Enum, IntEnum


class CardColor(Enum):
    Blue = 1
    Green = 2
    Red = 3


class Tag(Enum):
    Science = 1
    Building = 2
    Space = 3
    Power = 4
    Jovian = 5
    Earth = 6
    Plant = 7
    Microbe = 8
    Animal = 9
    Event = 10


class PlayerColor(Enum):
    Yellow = 1
    Green = 2
    Red = 3
    Blue = 4


class Phase(IntEnum):
    Development = 1
    Construction = 2
    Action = 3
    Production = 4
    Research = 5


class RoundStep(IntEnum):
    Planning = 1
    ResolvePhases = 2
    End = 3
