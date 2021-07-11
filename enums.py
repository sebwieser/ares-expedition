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


class PlayerAction(Enum):
    ChooseCorporation = 1,
    RedrawProjectCards = 2,
    SellProjectCards = 3,
    PlayGreenCard = 4,
    DrawProjectCard = 5,
    PlayRedOrBlueCard = 6,
    ChoosePhaseCard = 7,
    ResolveActionAbilities = 8,
    BuildGreenery = 9,
    RaiseTemperature = 10
    StandardActionBuildGreenery = 11,
    StandardActionRaiseTemperature = 12,
    StandardActionFlipOcean = 13,
    Produce = 14,
    Research = 15,
    DiscardDownTo10Cards = 16
