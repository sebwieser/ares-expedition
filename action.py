from abc import abstractmethod
from player import Player


class Action:
    def __init__(self):
        pass

    @abstractmethod
    def meets_conditions(self, player: Player) -> bool:
        pass

    @abstractmethod
    def play(self, player: Player) -> None:
        pass
