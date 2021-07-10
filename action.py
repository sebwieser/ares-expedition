from abc import abstractmethod, ABC
from player import Player


class Action(ABC):
    @abstractmethod
    def meets_conditions(self, player: Player) -> bool:
        raise NotImplementedError

    @abstractmethod
    def play(self, player: Player) -> None:
        raise NotImplementedError
