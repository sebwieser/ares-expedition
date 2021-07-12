from action import Action
from enums import Phase
from global_requirements import Oxygen
from player import Player


class SteelworksAction(Action):
    def play(self, player: Player) -> None:
        player.board.remove_heat(6)
        player.board.add_megacredits(2)
        player.increase_global_parameter(Oxygen)

    def meets_conditions(self, player: Player) -> bool:
        return player.board.heat >= 6


class CommunityGardensAction(Action):
    def play(self, player: Player) -> None:
        player.board.add_megacredits(2)
        if player.current_phase_card == Phase.Action:
            player.board.add_plants(1)

    def meets_conditions(self, player: Player) -> bool:
        return True


class WaterImportFromEuropaAction(Action):
    def meets_conditions(self, player: Player) -> bool:
        pass

    def play(self, player: Player) -> None:
        pass
