from typing import Type, Optional
from card import ProjectCard, CorporationCard, CardColor
from deck import Deck
from enums import PlayerColor, Phase
from exceptions import PhaseCardException, PhaseException
from game import Game
from global_requirements import GlobalParameter
from player_board import PlayerBoard


class Player:
    def __init__(self, name: str, color: PlayerColor):
        self.name = name
        self.game = None
        self.terraforming_rating: int = 5
        self.greenery_tokens: int = 0
        self.color = color
        self.project_cards = None
        self.starting_corporation_cards = None
        self.deck = None
        self.phase_cards: list[Phase] = [Phase.Development,
                                         Phase.Construction,
                                         Phase.Action,
                                         Phase.Production,
                                         Phase.Research]
        self.current_phase_card: Optional[Phase] = None
        self.corporation_card: Optional[CorporationCard] = None
        self.board: PlayerBoard = PlayerBoard()
        self.played_cards: list[ProjectCard] = list[ProjectCard]()

    def link_to_game(self, game: Game):
        self.game = game

    def assign_starting_corporations(self, corporations: list[CorporationCard]):
        self.starting_corporation_cards = corporations

    def assign_starting_project_cards(self, project_cards: list[ProjectCard]):
        self.project_cards = project_cards

    def give_access_to_project_deck(self, deck: Deck[ProjectCard]):
        self.deck = deck

    def increase_global_parameter(self, parameter_type: Type[GlobalParameter]):
        prize = self.game.global_requirements.increase_parameter(parameter_type, self.game.get_turn())
        prize.award_to_player(self)

    def add_terraforming_rating(self, points: int) -> int:
        self.terraforming_rating += points
        return self.terraforming_rating

    def add_greenery_token(self) -> int:
        self.greenery_tokens += 1
        return self.greenery_tokens

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
        self.project_cards.extend(drawn_cards)

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
