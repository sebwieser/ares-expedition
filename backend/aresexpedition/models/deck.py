import random
from typing import TypeVar, Generic
from card import ProjectCard, CorporationCard
from exceptions import GameException

T = TypeVar('T', ProjectCard, CorporationCard)


class Deck(Generic[T]):
    def __init__(self, cards: list[T]):
        self._cards = cards
        self._discard_pile: list[T] = list[T]()

    def shuffle(self) -> None:
        random.shuffle(self._cards)

    def count(self) -> int:
        return len(self._cards)

    def empty(self) -> bool:
        return len(self._cards) == 0

    def draw(self, amount: int) -> list[T]:
        drawn_cards = list[T]()
        deck_size = self.count()
        if deck_size < amount:
            drawn_cards += self.draw(deck_size)
            self._restore_discard_pile()
            if self.empty():
                return drawn_cards[T]
        drawn_cards += self._cards[:amount - len(drawn_cards)]
        del self._cards[:amount - len(drawn_cards)]
        return drawn_cards

    def discard(self, cards: list[T]) -> None:
        self._discard_pile.extend(cards)

    def _restore_discard_pile(self) -> None:
        if not self.empty():
            raise GameException("Cannot restore discard pile until the deck is empty.")
        self._cards.extend(self._discard_pile)
        self._discard_pile.clear()
        self.shuffle()
