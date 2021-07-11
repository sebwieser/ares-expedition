from abc import abstractmethod, ABC

from enums import Phase
from player import Player


class CardRequirements(ABC):
    def meets_conditions(self, player: Player) -> bool:
        return self._meets_color_conditions(player) and self._meets_custom_conditions(player)

    @abstractmethod
    def _meets_color_conditions(self, player: Player) -> bool:
        raise NotImplementedError

    @abstractmethod
    def _meets_custom_conditions(self, player: Player) -> bool:
        raise NotImplementedError


class GreenCardRequirements(CardRequirements, ABC):
    def _meets_color_conditions(self, player: Player) -> bool:
        return player.game.get_current_phase() == Phase.Development and not player.has_played_green_card


class RedBlueCardRequirements(CardRequirements, ABC):
    def _meets_color_conditions(self, player: Player) -> bool:
        return player.game.get_current_phase() == Phase.Construction \
               and (not player.has_played_red_or_blue_card
                    or player.is_eligible_for_bonus(Phase.Construction))


class DefaultGreenCardRequirements(GreenCardRequirements):
    def _meets_custom_conditions(self, player: Player) -> bool:
        return True


class DefaultRedBlueCardRequirements(RedBlueCardRequirements):
    def _meets_custom_conditions(self, player: Player) -> bool:
        return True
