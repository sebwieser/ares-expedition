class PlayerBoard:
    def __init__(self):
        self.megacredits = 0
        self.heat = 0
        self.plants = 0
        self.production_megacredits = 0
        self.production_cards = 0
        self.production_steel = 0
        self.production_titanium = 0
        self.production_heat = 0
        self.production_plants = 0

    def building_tag_discount(self) -> int:
        return 2*self.production_steel

    def space_tag_discount(self) -> int:
        return 3*self.production_titanium

    def add_megacredits(self, amount: int) -> None:
        self.megacredits += amount

    def add_heat(self, amount: int) -> None:
        self.heat += amount

    def add_plants(self, amount: int) -> None:
        self.plants += amount

    def remove_megacredits(self, amount: int) -> None:
        self.megacredits = max(0, self.megacredits - amount)

    def remove_heat(self, amount: int) -> None:
        self.heat = max(0, self.heat - amount)

    def remove_plants(self, amount: int) -> None:
        self.plants = max(0, self.plants - amount)

    def increase_megacredits_production(self, amount: int) -> None:
        self.production_megacredits += amount

    def increase_heat_production(self, amount: int) -> None:
        self.production_heat += amount

    def increase_plants_production(self, amount: int) -> None:
        self.production_plants += amount

    def increase_cards_production(self, amount: int) -> None:
        self.production_cards += amount

    def increase_steel_production(self, amount: int) -> None:
        self.production_steel += amount

    def increase_titanium_production(self, amount: int) -> None:
        self.production_titanium += amount
