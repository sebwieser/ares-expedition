import project_cards
import corporation_cards
from enums import Phase, RoundStep
from exceptions import GameException
from game_state import GameState
from global_requirements import *
import random
from deck import Deck, ProjectCard, CorporationCard
from dataclasses import dataclass


@dataclass
class Turn:
    round: int
    phase: Optional[Phase]
    step: RoundStep


class TurnManager:
    def __init__(self):
        self.turn = Turn(round=1, phase=None, step=RoundStep.Planning)
        self.phases: list[Phase] = list()
        self.is_game_start: bool = True

    def next_turn(self) -> Turn:
        """
        This method performs transitions between game rounds, phases and steps as per the rulebook
        and returns the next Turn. Turn is a game state consisting of round, phase and round step.

        :return: next Turn state
        """
        if self.is_game_start:
            self.is_game_start = False
            return self.turn
        # We advance the round step in two cases:
        #   1. If the turn has just started (Planning->ResolvePhases step transition)
        #   2. If current phase is the last one players picked for this round (ResolvePhases->End step transition)
        if self.turn.step == RoundStep.Planning \
                or (self.turn.step == RoundStep.ResolvePhases and self._is_last_phase()):
            return self._advance_step()
        # Else, if we are somewhere in the middle of ResolvePhases step, we iterate through chosen phases
        elif self.turn.step == RoundStep.ResolvePhases:
            return self._advance_phase()
        # Finally, if we are not in the Planning or ResolvePhases step, we must be in the End step,
        # in which case we should advance the game to the next round
        elif self.turn.step == RoundStep.End:
            return self._advance_round()
        # Something is wrong if we get here
        else:
            raise GameException(f"Error while advancing turn, unknown transition from {self.turn} occurred")

    def _is_last_phase(self) -> bool:
        return self.turn.phase == self.phases[-1]

    def set_phases(self, phases: list[Phase]):
        self.phases = phases

    def _advance_round(self) -> Turn:
        self.turn = Turn(self.turn.round + 1, None, RoundStep.Planning)
        self.phases.clear()
        return self.turn

    def _advance_step(self) -> Turn:
        self.turn = Turn(self.turn.round,
                         self.phases[0] if self.turn.step == RoundStep.Planning else None,
                         RoundStep((int(self.turn.step) + 1) % len(RoundStep)))
        return self.turn

    def _advance_phase(self) -> Turn:
        if self.turn.phase is None or self.phases.index(self.turn.phase) == self.phases[-1]:
            raise GameException("Phase cannot be changed.")
        self.turn = Turn(self.turn.round,
                         self.phases[self.phases.index(self.turn.phase) + 1],
                         self.turn.step)
        return self.turn


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
        self.round_step: Optional[RoundStep] = None
        self.final_turn: Optional[Turn] = None

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

    def get_current_turn(self) -> Turn:
        return self._turn_manager.turn

    def get_current_phase(self) -> Phase:
        return self._turn_manager.turn.phase

    def get_current_round(self) -> int:
        return self._turn_manager.turn.round

    def get_current_step(self) -> RoundStep:
        return self._turn_manager.turn.step

    def is_game_start(self) -> bool:
        return self._turn_manager.is_game_start

    # TODO: need to set the final_turn when global requirements get maxed out
    def is_finished(self) -> bool:
        return self.global_requirements.end_game_condition_met() and self.get_current_phase() != self.final_turn.phase

    def advance(self) -> GameState:
        raise NotImplementedError

    def _randomize_player_order(self) -> None:
        random.shuffle(self.players)
