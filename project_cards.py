from action_impls import *
from card import ProjectCard, BlueProjectCard
from enums import Tag

Steelworks = BlueProjectCard(name="Steelworks", cost=15, points=1, tags=[Tag.Building], action=SteelworksAction())
CommunityGardens = BlueProjectCard(name="Community Gardens", cost=20, tags=[Tag.Plant], action=CommunityGardensAction())
WaterImportFromEuropa = BlueProjectCard(name="Water Import From Europa", cost=22, tags=[Tag.Space, Tag.Jovian],
                                        action=WaterImportFromEuropaAction())

ALL_PROJECT_CARDS: list[ProjectCard] = [
    Steelworks,
    CommunityGardens,
    WaterImportFromEuropa
]
