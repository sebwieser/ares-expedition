import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Type, Optional
from exceptions import GlobalRequirementException
from game import Turn
from player import Player


class GlobalParameterColor(Enum):
    Purple = 1
    Red = 2
    Yellow = 3
    White = 4


@dataclass
class GlobalParameterPrize:
    award_tr: int = 1
    megacredits: int = 0
    cards: int = 0
    plants: int = 0

    def award_to_player(self, player: Player):
        if self.award_tr:
            player.add_terraforming_rating(1)
        if self.plants > 0:
            player.board.add_plants(self.plants)
        if self.megacredits > 0:
            player.board.add_megacredits(self.megacredits)
        if self.cards > 0:
            player.draw_project_cards(self.cards)


class GlobalParameter(ABC):
    def __init__(self, minimum: int, maximum: int, step: int):
        self.value = minimum
        self.minimum = minimum
        self.maximum = maximum
        self.step = step
        self.maxed_on_turn: Optional[Turn] = None

    def increase(self, turn: Turn) -> GlobalParameterPrize:
        self.value = min(self.maximum, self.value + self.step)
        if self.is_maxed() and self.maxed_on_turn is None:
            self.maxed_on_turn = turn
        if self.is_complete(turn):
            return self._get_residual_prize()
        return self._get_full_prize()

    def is_complete(self, turn: Turn):
        return self.maxed_on_turn is not None and self.maxed_on_turn != turn

    def is_maxed(self) -> bool:
        return self.value == self.maximum

    @abstractmethod
    def _get_full_prize(self) -> GlobalParameterPrize:
        raise NotImplementedError

    @abstractmethod
    def _get_residual_prize(self) -> GlobalParameterPrize:
        raise NotImplementedError


class Temperature(GlobalParameter):
    def __init__(self, minimum=-30, maximum=8, step=2):
        super().__init__(minimum, maximum, step)

    def _get_full_prize(self) -> GlobalParameterPrize:
        return GlobalParameterPrize()

    def _get_residual_prize(self) -> GlobalParameterPrize:
        return GlobalParameterPrize(award_tr=False)

    def get_color(self) -> GlobalParameterColor:
        if self.value < -18:
            return GlobalParameterColor.Purple
        elif self.value < -8:
            return GlobalParameterColor.Red
        elif self.value < 2:
            return GlobalParameterColor.Yellow
        else:
            return GlobalParameterColor.White

    def compare_to_color(self, color: GlobalParameterColor):
        """
        :param color: color threshold to compare current temperature to
        :return: Returns 1 if temperature is at higher level than given color, 0 if equal or -1 if less
        """
        temperature_color = self.get_color()
        return 0 if temperature_color == color else 1 if temperature_color > color else -1


class Oxygen(GlobalParameter):
    def __init__(self, minimum: int = 0, maximum: int = 14, step: int = 1):
        super().__init__(minimum, maximum, step)

    def _get_full_prize(self) -> GlobalParameterPrize:
        return GlobalParameterPrize()

    def _get_residual_prize(self) -> GlobalParameterPrize:
        return GlobalParameterPrize(award_tr=False)

    def get_color(self) -> GlobalParameterColor:
        if self.value < 3:
            return GlobalParameterColor.Purple
        elif self.value < 7:
            return GlobalParameterColor.Red
        elif self.value < 12:
            return GlobalParameterColor.Yellow
        else:
            return GlobalParameterColor.White

    def compare_to_color(self, color: GlobalParameterColor):
        """
        :param color: color threshold to compare current oxygen to
        :return: Returns 1 if oxygen is at higher level than given color, 0 if equal or -1 if less
        """
        oxygen_color = self.get_color()
        return 0 if oxygen_color == color else 1 if oxygen_color > color else -1


class Oceans(GlobalParameter):
    OCEAN_PRIZES: list[GlobalParameterPrize] = [
        GlobalParameterPrize(megacredits=2, plants=1),
        GlobalParameterPrize(megacredits=1, cards=1),
        GlobalParameterPrize(plants=2),
        GlobalParameterPrize(plants=2),
        GlobalParameterPrize(megacredits=4),
        GlobalParameterPrize(cards=1),
        GlobalParameterPrize(cards=1),
        GlobalParameterPrize(plants=1, cards=1),
        GlobalParameterPrize(megacredits=1, plants=1)
    ]

    def __init__(self, minimum: int = 0, maximum: int = 9, step: int = 1):
        super().__init__(minimum, maximum, step)
        random.shuffle(Oceans.OCEAN_PRIZES)
        self.last_prize: Optional[GlobalParameterPrize] = None

    def _get_full_prize(self) -> GlobalParameterPrize:
        next_prize: GlobalParameterPrize = Oceans.OCEAN_PRIZES.pop(0) \
            if len(Oceans.OCEAN_PRIZES) > 0 \
            else self.last_prize
        self.last_prize = next_prize
        return next_prize

    def _get_residual_prize(self) -> GlobalParameterPrize:
        return GlobalParameterPrize(award_tr=False)


class GlobalRequirements:
    def __init__(self):
        self.parameters: list[GlobalParameter] = [Temperature(), Oxygen(), Oceans()]

    def _get_parameter(self, parameter_type: Type[GlobalParameter]) -> GlobalParameter:
        parameter = next((p for p in self.parameters if isinstance(p, parameter_type)), None)
        if parameter is None:
            raise GlobalRequirementException(f"Invalid global parameter type: {parameter_type}")
        return parameter

    def increase_parameter(self, parameter_type: Type[GlobalParameter], turn: Turn) -> GlobalParameterPrize:
        parameter = self._get_parameter(parameter_type)
        return parameter.increase(turn)

    def end_game_condition_met(self):
        for p in self.parameters:
            if not p.is_maxed():
                return False
        return True

    def parameter_complete(self, parameter_type: Type[GlobalParameter], turn: Turn):
        parameter = self._get_parameter(parameter_type)
        return parameter.is_complete(turn)
