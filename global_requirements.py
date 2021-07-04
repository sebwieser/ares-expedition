from enum import Enum


class GlobalParameterColor(Enum):
    Purple = 1
    Red = 2
    Yellow = 3
    White = 4


class GlobalRequirements:
    MAX_TEMPERATURE: int = 8
    MAX_OXYGEN: int = 14
    MAX_OCEANS: int = 9
    STEP_TEMPERATURE = 2
    STEP_OXYGEN = 1
    STEP_OCEAN = 1

    def __init__(self):
        self.temperature = -30
        self.oxygen = 0
        self.oceans = 0

    def increase_temperature(self) -> None:
        self.temperature = min(GlobalRequirements.MAX_TEMPERATURE,
                               self.temperature + GlobalRequirements.STEP_TEMPERATURE)

    def increase_oxygen(self) -> None:
        self.oxygen = min(GlobalRequirements.MAX_OXYGEN, self.oxygen + GlobalRequirements.STEP_OXYGEN)

    def flip_ocean(self) -> None:
        self.oceans = min(GlobalRequirements.MAX_OCEANS, self.oceans + GlobalRequirements.STEP_OCEAN)

    def end_game_condition_met(self) -> bool:
        return self.is_oxygen_maxed() \
               and self.is_temperature_maxed() \
               and self.are_oceans_maxed()

    def is_temperature_maxed(self) -> bool:
        return self.temperature == GlobalRequirements.MAX_TEMPERATURE

    def is_oxygen_maxed(self) -> bool:
        return self.oxygen == GlobalRequirements.MAX_OXYGEN

    def are_oceans_maxed(self) -> bool:
        return self.oceans == GlobalRequirements.MAX_OCEANS

    def temperature_color(self) -> GlobalParameterColor:
        if self.temperature < -18:
            return GlobalParameterColor.Purple
        elif self.temperature < -8:
            return GlobalParameterColor.Red
        elif self.temperature < 2:
            return GlobalParameterColor.Yellow
        else:
            return GlobalParameterColor.White

    def oxygen_color(self) -> GlobalParameterColor:
        if self.oxygen < 3:
            return GlobalParameterColor.Purple
        elif self.oxygen < 7:
            return GlobalParameterColor.Red
        elif self.oxygen < 12:
            return GlobalParameterColor.Yellow
        else:
            return GlobalParameterColor.White

    def compare_to_temperature_color(self, color: GlobalParameterColor):
        """
        :param color: color threshold to compare current temperature to
        :return: Returns 1 if temperature is at higher level than given color, 0 if equal or -1 if less
        """
        temperature_color = self.temperature_color()
        return 0 if temperature_color == color else 1 if temperature_color > color else -1

    def compare_to_oxygen_color(self, color: GlobalParameterColor):
        """
        :param color: color threshold to compare current oxygen to
        :return: Returns 1 if oxygen is at higher level than given color, 0 if equal or -1 if less
        """
        oxygen_color = self.oxygen_color()
        return 0 if oxygen_color == color else 1 if oxygen_color > color else -1