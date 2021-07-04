from card import *


class PhaseCardException(Exception):
    pass


class PhaseException(Exception):
    pass


class PlayerColor(Enum):
    Yellow = 1
    Green = 2
    Red = 3
    Blue = 4


class Phase(Enum):
    Development = 1
    Construction = 2
    Action = 3
    Production = 4
    Research = 5


class RoundStep(Enum):
    Planning = 1
    ResolvePhases = 2
    End = 3


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


class Player:
    def __init__(self, color: PlayerColor, project_cards: list[ProjectCard], corporation_cards: list[CorporationCard], deck: ProjectDeck):
        self.terraforming_rating = 5
        self.color = color
        self.project_cards = project_cards
        self.starting_corporation_cards = corporation_cards
        self.deck = deck
        self.phase_cards: list[Phase] = [Phase.Development,
                                         Phase.Construction,
                                         Phase.Action,
                                         Phase.Production,
                                         Phase.Research]
        self.current_phase_card: Phase = None
        self.corporation_card: CorporationCard = None
        self.board: PlayerBoard = PlayerBoard()
        self.played_cards: list[ProjectCard] = list[ProjectCard]()

    def add_terraforming_rating(self, points: int) -> int:
        self.terraforming_rating += points
        return self.terraforming_rating

    def deduct_terraforming_rating(self, points: int) -> int:
        self.terraforming_rating = max(0, self.terraforming_rating - points)
        return self.terraforming_rating

    def produce(self) -> None:
        self.board.add_heat(self.board.production_heat)
        self.board.add_plants(self.board.production_plants)
        self.board.add_megacredits(self.board.production_megacredits)
        self.draw_cards(self.board.production_cards)

    def draw_cards(self, amount: int) -> None:
        drawn_cards = self.deck.draw(amount)
        self.project_cards.append(drawn_cards)

    def choose_phase_card(self, phase_card: Phase) -> Phase:
        if phase_card == self.current_phase_card:
            raise PhaseCardException("Cannot play the same phase card twice in a row.")
        self.current_phase_card = phase_card
        return self.current_phase_card

    def play_green_card(self, card: ProjectCard) -> None:
        if card.color != CardColor.Green:
            raise PhaseException(f"Expected a {CardColor.Green} card, but got: {card.color}")
        card.play(self)

    def play_blue_or_red_card(self, card: ProjectCard) -> None:
        if card.color == CardColor.Green:
            raise PhaseException(f"Expected a {CardColor.Red} or {CardColor.Blue} card, but got: {CardColor.Green}")
        card.play(self)


