from typing import Optional

from action import Action
from card_requirements import CardRequirements, DefaultGreenCardRequirements, DefaultRedBlueCardRequirements
from effect import Effect
from enums import Tag, CardColor, Phase
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
    def __init__(self, name: str, tags: list[Tag], starting_resources: Action, action: Optional[Action] = None,
                 effect: Optional[Effect] = None):
        super().__init__(name, tags, action, effect)
        self.starting_resources = starting_resources

    def play(self, player: Player):
        self.starting_resources.play(player)


class ProjectCard(Card, ABC):
    def __init__(self, name: str, cost: int, color: CardColor, requirements: CardRequirements, points: int = 0,
                 tags: list[Tag] = None, action: Action = None, effect: Effect = None):
        super().__init__(name, tags, action, effect)
        self.cost = cost
        self.points = points
        self.requirements = requirements
        self.color = color
        self.resources: int = 0

    @abstractmethod
    def play(self, player: Player):
        raise NotImplementedError

    def player_meets_conditions(self, player: Player) -> bool:
        return self.requirements.meets_conditions(player)


class GreenProjectCard(ProjectCard, ABC):
    def __init__(self, name: str, cost: int, requirements: CardRequirements = DefaultGreenCardRequirements(),
                 points: int = 0, tags: list[Tag] = None, action: Action = None, effect: Effect = None):
        super().__init__(name, cost, CardColor.Green, requirements, points, tags, action, effect)


class BlueProjectCard(ProjectCard, ABC):
    def __init__(self, name: str, cost: int, requirements: CardRequirements = DefaultRedBlueCardRequirements(),
                 points: int = 0, tags: list[Tag] = None, action: Action = None, effect: Effect = None):
        super().__init__(name, cost, CardColor.Blue, requirements, points, tags, action, effect)
        self.action_played_this_round: bool = False

    def is_action_playable(self, player: Player) -> bool:
        return self.action is not None and self.action.meets_conditions(player) and \
               (not self.action_played_this_round or player.is_eligible_for_bonus(Phase.Action))


class RedProjectCard(ProjectCard, ABC):
    def __init__(self, name: str, cost: int, requirements: CardRequirements = DefaultRedBlueCardRequirements(),
                 points: int = 0, tags: list[Tag] = None, action: Action = None, effect: Effect = None):
        super().__init__(name, cost, CardColor.Red, requirements, points, tags, action, effect)
