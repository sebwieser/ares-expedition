from typing import Optional

from action import Action
from card_requirements import CardRequirements
from effect import Effect
from enums import Tag, CardColor
from player import Player
from abc import ABC, abstractmethod


class Card(ABC):
    def __init__(self, name: str, tags: list[Tag], action: Optional[Action], effect: Optional[Effect]):
        self.name = name
        self.tags = tags
        self.action = action
        self.effect = effect

    @abstractmethod
    def play(self, player: Player):
        raise NotImplementedError


class CorporationCard(Card):
    def __init__(self, name: str, tags: list[Tag], starting_resources: Action, action: Optional[Action],
                 effect: Optional[Effect]):
        super().__init__(name, tags, action, effect)
        self.starting_resources = starting_resources

    def play(self, player: Player):
        self.starting_resources.play(player)


class ProjectCard(Card):
    def __init__(self, name: str, cost: int, color: CardColor, points: int = 0,
                 requirements: Optional[CardRequirements] = None, tags: list[Tag] = None,
                 action: Action = None, effect: Effect = None):
        super().__init__(name, tags, action, effect)
        self.cost = cost
        self.points = points
        self.requirements = requirements
        self.color = color
        self.resources: int = 0

    def play(self, player: Player):
        pass

    def player_meets_conditions(self, player: Player) -> bool:
        if self.requirements is not None:
            return self.requirements.meets_conditions(player)
        return True
