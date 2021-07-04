from typing import Callable
from main import Player
from enum import Enum
import abc
import random

class CardRequirement:
    pass


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


class Card:
    __metaclass__ = abc.ABCMeta

    def __init__(self, name: str, tags: list[Tag], action: Callable[[Player], None], effect: Callable[[Player], None]):
        self.name = name
        self.tags = tags
        self.action = action
        self.effect = effect

    @abc.abstractmethod
    def play(self, player: Player):
        return


class CorporationCard(Card):
    def __init__(self, name: str, tags: list[Tag], starting_resources_func: Callable, action: Callable[[Player], None],
                 effect: Callable[[Player], None]):
        Card.__init__(name, tags, action, effect)
        self.add_starting_resources = starting_resources_func

    def play(self, player: Player):
        self.add_starting_resources(player)


class ProjectCard(Card):
    def __init__(self, name: str, cost: int, requirement: CardRequirement, tags: list[Tag], color: CardColor,
                 action: Callable[[Player], None], effect: Callable[[Player], None]):
        Card.__init__(name, tags, action, effect)
        self.cost = cost
        self.requirement = requirement
        self.color = color

    def play(self, player: Player):
        pass


class Deck:
    def __init__(self, cards: list[Card]):
        self._cards = cards
        self._discard_pile: list[Card] = list[Card]()

    def shuffle(self) -> None:
        random.shuffle(self._cards)

    def count(self) -> int:
        return len(self._cards)

    def draw(self, amount: int) -> list[Card]:
        drawn_cards = list[Card]()
        deck_size = self.count()
        if deck_size < amount:
            drawn_cards += self.draw(deck_size)
            self._restore_discard_pile()
            self.shuffle()
        drawn_cards += self._cards[:amount - len(drawn_cards)]
        del self._cards[:amount - len(drawn_cards)]
        return drawn_cards

    def discard(self, cards: list[Card]) -> None:
        self._discard_pile.extend(cards)

    def _restore_discard_pile(self):
        self._cards.extend(self._discard_pile)
        self._discard_pile.clear()


class CorporationsDeck(Deck):
    def __init__(self, cards: list[CorporationCard]):
        Deck.__init__(cards)


class ProjectDeck(Deck):
    def __init__(self, cards: list[ProjectCard]):
        Deck.__init__(cards)




