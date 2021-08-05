from abc import ABC
from math import floor

from card import ProjectCard


class Points(ABC):
    def __init__(self, card: ProjectCard):
        self.card = card

    def get(self):
        raise NotImplementedError


class ResourcesOnCard(Points):
    def __init__(self, card: ProjectCard, n_for_point: int):
        super().__init__(card)
        self.n = n_for_point

    def get(self):
        return floor(self.card.resources/self.n)
