from action_impls import *
from card import ProjectCard
from enums import Tag, CardColor

Steelworks = ProjectCard(name="Steelworks", cost=15, color=CardColor.Blue, points=1, tags=[Tag.Building],
                         action=SteelworksAction())
CommunityGardens = ProjectCard(name="Community Gardens", cost=20, color=CardColor.Blue, tags=[Tag.Plant],
                               action=CommunityGardensAction())
WaterImportFromEuropa = ProjectCard(name="Water Import From Europa", cost=22, color=CardColor.Blue,
                                    tags=[Tag.Space, Tag.Jovian], action=WaterImportFromEuropaAction())

ALL_PROJECT_CARDS: list[ProjectCard] = [
    Steelworks,
    CommunityGardens,
    WaterImportFromEuropa
]
