from typing import Optional

from action import Action
from effect import Effect
from enums import Tag, CardColor
from player import Player
from abc import ABC, abstractmethod


class CardRequirement:
    pass


class Card(ABC):
    def __init__(self, name: str, tags: list[Tag], action: Optional[Action], effect: Optional[Effect]):
        self.name = name
        self.tags = tags
        self.action = action
        self.effect = effect

    @abstractmethod
    def play(self, player: Player):
        pass


class CorporationCard(Card):
    def __init__(self, name: str, tags: list[Tag], starting_resources: Action, action: Optional[Action],
                 effect: Optional[Effect]):
        super().__init__(name, tags, action, effect)
        self.add_starting_resources = starting_resources

    def play(self, player: Player):
        self.add_starting_resources.play(player)


class ProjectCard(Card):
    def __init__(self, name: str, cost: int, color: CardColor, points: int = 0, requirement: CardRequirement = None,
                 tags: list[Tag] = None, action: Action = None, effect: Effect = None):
        super().__init__(name, tags, action, effect)
        self.cost = cost
        self.points = points
        self.requirement = requirement
        self.color = color
        self.resources: int = 0

    def play(self, player: Player):
        pass
