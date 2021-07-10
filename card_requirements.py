from abc import abstractmethod, ABC
from player import Player


class CardRequirements(ABC):
    @abstractmethod
    def meets_conditions(self, player: Player) -> bool:
        raise NotImplementedError
