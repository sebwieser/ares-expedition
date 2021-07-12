from typing import Type, Optional
from card import ProjectCard, CorporationCard, CardColor, BlueProjectCard
from deck import Deck
from enums import PlayerColor, Phase, PlayerAction, RoundStep
from exceptions import GameException
from game import Game
from global_requirements import GlobalParameter
from player_board import PlayerBoard


class Player:
    def __init__(self, name: str, color: PlayerColor):
        self.name: str = name
        self.game: Optional[Game] = None
        self.terraforming_rating: int = 5
        self.greenery_tokens: int = 0
        self.color: PlayerColor = color
        self.project_cards: Optional[list[ProjectCard]] = None
        self.starting_corporation_cards: Optional[list[CorporationCard]] = None
        self.project_deck: Optional[Deck[ProjectCard]] = None
        self.corporation_deck: Optional[Deck[CorporationCard]] = None
        self.phase_cards: list[Phase] = [Phase.Development,
                                         Phase.Construction,
                                         Phase.Action,
                                         Phase.Production,
                                         Phase.Research]
        self.current_phase_card: Optional[Phase] = None
        self.last_phase_card: Optional[Phase] = None
        self.corporation_card: Optional[CorporationCard] = None
        self.board: PlayerBoard = PlayerBoard()
        self.played_project_cards: list[ProjectCard] = list[ProjectCard]()
        self.redrew_starting_project_cards: bool = False
        self.has_picked_corporation: bool = False
        self.has_picked_phase_card: bool = False
        self.has_played_green_card: bool = False
        self.has_played_red_or_blue_card: bool = False
        self.used_phase_bonus: bool = False
        self.has_produced: bool = False
        self.has_researched: bool = False
        self.greenery_plant_cost: int = Game.DEFAULT_GREENERY_PLANT_COST
        self.greenery_mc_cost: int = Game.DEFAULT_GREENERY_MC_COST
        self.temperature_heat_cost: int = Game.DEFAULT_TEMPERATURE_HEAT_COST
        self.temperature_mc_cost: int = Game.DEFAULT_TEMPERATURE_MC_COST
        self.ocean_mc_cost: int = Game.DEFAULT_OCEAN_MC_COST
        self.available_actions: list[PlayerAction] = list[PlayerAction]()

    def is_eligible_for_bonus(self, phase: Phase):
        return self.current_phase_card == phase and self.used_phase_bonus

    def use_phase_bonus(self, phase: Phase):
        if not self.is_eligible_for_bonus(phase):
            raise GameException(f"Player not eligible for {phase} bonus.")
        self.used_phase_bonus = True

    def link_to_game(self, game: Game) -> None:
        self.game = game

    def assign_starting_corporations(self, corporations: list[CorporationCard]) -> None:
        self.starting_corporation_cards = corporations

    def assign_starting_project_cards(self, project_cards: list[ProjectCard]) -> None:
        self.project_cards = project_cards

    def give_access_to_project_deck(self, deck: Deck[ProjectCard]) -> None:
        self.project_deck = deck

    def give_access_to_corporation_deck(self, deck: Deck[CorporationCard]) -> None:
        self.corporation_deck = deck

    def choose_corporation(self, card: CorporationCard) -> None:
        """
        Sets the corporation card as chosen for the remainder of the game.

        :param card: corporation card to keep
        """
        self.corporation_card = card
        self.corporation_card.play(self)
        self.has_picked_corporation = True

    def _discard_project_cards(self, cards: list[ProjectCard]) -> int:
        """
        Discards the listed project cards from player's hand.

        :param cards: List of project cards to discard
        :return: Number of discarded cards
        """
        self.project_deck.discard(cards)
        return len(cards)

    def sell_project_cards(self, cards: list[ProjectCard]) -> int:
        """
        Sells the listed cards. Cards are discarded and player receives 3 Megacredits for each card in the list.

        :param cards: list of project cards player wants to sell
        :return: Number of sold cards
        """
        num_cards = self._discard_project_cards(cards)
        self.board.add_megacredits(3*num_cards)
        return num_cards

    def redraw_starting_project_cards(self, project_cards: list[ProjectCard]) -> int:
        """
        Listed project cards will be discarded from player's hand without receiving any prize.
        Player will then draw (receive) the same number of new project cards from deck.
        This can be done only once per game and only before choosing the starting corporation card.

        :param project_cards: Project cards to discard
        :return: Number of discarded (but also drawn) cards
        """
        if self.has_picked_corporation:
            raise GameException("Cannot redraw starting project cards after choosing the corporation.")
        if self.redrew_starting_project_cards:
            raise GameException("Cannot redraw starting project cards more than once.")
        amount = self._discard_project_cards(project_cards)
        self.draw_project_cards(amount)
        self.redrew_starting_project_cards = True
        return amount

    def increase_global_parameter(self, parameter_type: Type[GlobalParameter]) -> None:
        prize = self.game.global_requirements.increase_parameter(parameter_type, self.game.get_current_turn())
        prize.award_to_player(self)

    def add_terraforming_rating(self, points: int) -> int:
        self.terraforming_rating += points
        return self.terraforming_rating

    def add_greenery_token(self) -> int:
        self.greenery_tokens += 1
        return self.greenery_tokens

    def deduct_terraforming_rating(self, points: int) -> int:
        """
        Deducts TR from player. Cannot go below 0.

        :param points: Number of TR points to deduct.
        :return: Player's total TR after deduction
        """
        self.terraforming_rating = max(0, self.terraforming_rating - points)
        return self.terraforming_rating

    def get_total_vp(self) -> int:
        """
        Returns player's current victory point total.
        :return: Number of player's VP
        """
        raise NotImplementedError

    def produce(self) -> None:
        """
        Performs production step for the player.

        :raises GameException: if outside the `Phase.Production` phase
        """
        if not self.is_eligible_for_action(PlayerAction.Produce):
            raise GameException(f"Cannot perform action {PlayerAction.Produce}.")
        self.board.add_heat(self.board.production_heat)
        self.board.add_plants(self.board.production_plants)
        self.board.add_megacredits(self.board.production_megacredits)
        self.draw_project_cards(self.board.production_cards)
        self.has_produced = True

    def draw_project_cards(self, amount: int) -> int:
        """
        Draws cards from project deck to player's hand.

        :param amount: Number of cards to draw
        :return: Number of drawn cards (might be less than intended if the deck is thinned)
        """
        drawn_cards = self.project_deck.draw(amount)
        self.project_cards.extend(drawn_cards)
        return len(drawn_cards)

    def get_project_hand_size(self) -> int:
        return len(self.project_cards)

    def choose_phase_card(self, phase_card: Phase) -> Phase:
        """
        Sets the chosen phase card for this round.

        :param phase_card: Chosen phase card
        :return: Chosen phase card
        :raises GameException: if player chose the same card two rounds in a row,
        or if the player chose the phase card this round.
        """
        if self.has_picked_phase_card:
            raise GameException("Player already chose the phase card this round.")
        if phase_card == self.last_phase_card:
            raise GameException("Cannot play the same phase card twice in a row.")
        self.last_phase_card = self.current_phase_card
        self.current_phase_card = phase_card
        self.has_picked_phase_card = True
        return self.current_phase_card

    def play_project_card(self, card: ProjectCard) -> None:
        """
        Tries to play the project card.
        If successful, player will have been deducted the cost discounted for bonuses, if any.
        Player will receive all instant card bonuses, if any.

        :param card: Project card to play
        :raises GameException: if the player doesn't meet requirements for playing the card.
        """
        if not card.player_meets_conditions(self):
            raise GameException(f"Requirements for playing the card {card} not met.")
        card.play(self)
        self._set_played_color(card.color)
        self.played_project_cards += card
        self.project_cards.remove(card)

    def _set_played_color(self, card_color: CardColor) -> None:
        if card_color == CardColor.Green:
            self.has_played_green_card = True
        else:
            self.has_played_red_or_blue_card = True

    def get_playable_cards(self) -> list[ProjectCard]:
        return [c for c in self.project_cards if c.player_meets_conditions(self)]

    def get_available_actions(self) -> list[PlayerAction]:
        if self.game.is_finished():
            return []
        if self.game.is_game_start():
            return self._get_game_start_actions()
        phase, step = self.game.get_current_phase(), self.game.get_current_step()
        actions: list[PlayerAction] = []
        # Players can sell project cards at any time, given their hand isn't empty
        if self.get_project_hand_size() > 0:
            actions += PlayerAction.SellProjectCards
        # Other actions depend on the current step, phase and global requirements status:
        if step == RoundStep.Planning:
            actions.extend(self._get_planning_actions())
        elif step == RoundStep.ResolvePhases:
            if phase == Phase.Development:
                actions.extend(self._get_development_phase_actions())
            elif phase == Phase.Construction:
                actions.extend(self._get_construction_phase_actions())
            elif phase == Phase.Action:
                actions.extend(self._get_action_phase_actions())
            elif phase == Phase.Production:
                actions.extend(self._get_production_phase_actions())
            elif phase == Phase.Research:
                actions.extend(self._get_research_phase_actions())
        elif step == RoundStep.End:
            actions.extend(self._get_end_actions())
        else:
            raise GameException("Unknown game state detected.")
        return actions

    def get_cards_with_playable_actions(self) -> list[BlueProjectCard]:
        return [card for card in self.played_project_cards
                if isinstance(card, BlueProjectCard) and card.is_action_playable(self)]

    def _get_action_phase_actions(self) -> list[PlayerAction]:
        actions: list[PlayerAction] = []
        if len(self.get_cards_with_playable_actions()) > 0:
            actions += PlayerAction.ResolveActionAbilities
        if self.board.plants >= self.greenery_plant_cost:
            actions += PlayerAction.BuildGreenery
        if self.board.heat >= self.temperature_heat_cost:
            actions += PlayerAction.RaiseTemperature
        if self.board.megacredits >= self.greenery_mc_cost:
            actions += PlayerAction.StandardActionBuildGreenery
        if self.board.megacredits >= self.temperature_mc_cost:
            actions += PlayerAction.StandardActionFlipOcean
        if self.board.megacredits >= self.ocean_mc_cost:
            actions += PlayerAction.StandardActionRaiseTemperature
        return actions

    def _get_construction_phase_actions(self) -> list[PlayerAction]:
        actions: list[PlayerAction] = []
        if len(self.get_playable_cards()) > 0:
            actions += PlayerAction.PlayRedOrBlueCard
        if self.is_eligible_for_bonus(Phase.Construction):
            actions += PlayerAction.DrawProjectCard
        return actions

    def _get_development_phase_actions(self) -> list[PlayerAction]:
        actions: list[PlayerAction] = []
        if len(self.get_playable_cards()) > 0:
            actions += PlayerAction.PlayGreenCard
        return actions

    def _get_planning_actions(self) -> list[PlayerAction]:
        actions: list[PlayerAction] = []
        if not self.has_picked_phase_card:
            actions += PlayerAction.ChoosePhaseCard
        return actions

    def _get_game_start_actions(self) -> list[PlayerAction]:
        actions: list[PlayerAction] = list()
        if not self.has_picked_corporation:
            actions += PlayerAction.ChooseCorporation
            if not self.redrew_starting_project_cards:
                actions += PlayerAction.RedrawProjectCards
        return actions

    def _get_production_phase_actions(self) -> list[PlayerAction]:
        return [PlayerAction.Produce] if not self.has_produced else []

    def _get_research_phase_actions(self) -> list[PlayerAction]:
        return [PlayerAction.Research] if not self.has_researched else []

    def _get_end_actions(self) -> list[PlayerAction]:
        return [PlayerAction.DiscardDownTo10Cards] if self.get_project_hand_size() > 10 else []

    def is_eligible_for_action(self, player_action: PlayerAction) -> bool:
        return player_action in self.available_actions
