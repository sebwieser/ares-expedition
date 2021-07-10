import project_cards
import corporation_cards
from enums import Phase
from global_requirements import *
import random
from deck import Deck, ProjectCard, CorporationCard
from dataclasses import dataclass


@dataclass
class Turn:
    round: int
    phase: Optional[Phase]


class TurnManager:
    def __init__(self):
        self.turn = Turn(round=1, phase=None)
        self.chosen_phases: list[Phase] = list()

    def next_turn(self):
        if self._next_phase() is None:
            return Turn(self._next_round(), None)
        else:
            return Turn(self.turn.round, self._next_phase())

    def set_next_round_phases(self, phases: list[Phase]):
        self.chosen_phases = phases

    def _next_round(self) -> int:
        return self.turn.round + 1

    def _next_phase(self) -> Optional[Phase]:
        if len(self.chosen_phases) == 0 or self.chosen_phases[-1] == self.turn.phase:
            self.chosen_phases = list[Phase]()
            return None
        return self.chosen_phases[self.chosen_phases.index(Turn.phase)+1]


class Game:
    def __init__(self, players: list[Player],
                 banned_corporations: Optional[list[CorporationCard]],
                 banned_projects: Optional[list[ProjectCard]]):
        self.global_requirements: GlobalRequirements = GlobalRequirements()
        self.players = players
        self._turn_manager = TurnManager()
        self.corporation_deck: Optional[Deck[CorporationCard]] = None
        self.project_deck: Optional[Deck[ProjectCard]] = None
        self.banned_corporations = banned_corporations
        self.banned_projects = banned_projects

    def start(self):
        self._randomize_player_order()
        self._initialize_corporations_deck()
        self._initialize_project_deck()
        self._initialize_players()

    def _initialize_players(self):
        for p in self.players:
            p.link_to_game(self)
            p.give_access_to_project_deck(self.project_deck)
            p.give_access_to_corporation_deck(self.corporation_deck)
            p.assign_starting_corporations(self.corporation_deck.draw(2))
            p.assign_starting_project_cards(self.project_deck.draw(8))

    def _initialize_project_deck(self):
        projects: list[ProjectCard] = [project for project in project_cards.ALL_PROJECT_CARDS
                                       if project not in self.banned_projects]
        self.project_deck = Deck[ProjectCard](projects)
        self.project_deck.shuffle()

    def _initialize_corporations_deck(self):
        corporations: list[CorporationCard] = [corporation for corporation in corporation_cards.ALL_CORPORATION_CARDS
                                               if corporation not in self.banned_corporations]
        self.corporation_deck = Deck[CorporationCard](corporations)
        self.corporation_deck.shuffle()

    def get_turn(self) -> Turn:
        return self._turn_manager.turn

    def get_phase(self) -> Phase:
        return self._turn_manager.turn.phase

    def advance(self):
        pass

    def _randomize_player_order(self) -> None:
        random.shuffle(self.players)
