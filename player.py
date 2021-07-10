from typing import Type, Optional
from card import ProjectCard, CorporationCard, CardColor
from deck import Deck
from enums import PlayerColor, Phase
from exceptions import GameException
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
        if self.corporation_card is not None:
            raise GameException("Cannot redraw project cards after choosing the starting corporation.")
        amount = self._discard_project_cards(project_cards)
        self.draw_project_cards(amount)
        return amount

    def increase_global_parameter(self, parameter_type: Type[GlobalParameter]) -> None:
        prize = self.game.global_requirements.increase_parameter(parameter_type, self.game.get_turn())
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
        current_phase = self.game.get_phase()
        if current_phase != Phase.Production:
            raise GameException(f"Cannot produce outside the {Phase.Production} phase.")
        self.board.add_heat(self.board.production_heat)
        self.board.add_plants(self.board.production_plants)
        self.board.add_megacredits(self.board.production_megacredits)
        self.draw_project_cards(self.board.production_cards)

    def draw_project_cards(self, amount: int) -> int:
        """
        Draws cards from project deck to player's hand.

        :param amount: Number of cards to draw
        :return: Number of drawn cards (might be less than intended if the deck is thinned)
        """
        drawn_cards = self.project_deck.draw(amount)
        self.project_cards.extend(drawn_cards)
        return len(drawn_cards)

    def choose_phase_card(self, phase_card: Phase) -> Phase:
        """
        Sets the chosen phase card for this round.

        :param phase_card: Chosen phase card
        :return: Chosen phase card
        :raises GameException: if player chose the same card two rounds in a row,
        or if the player chose the phase card this round.
        """
        if self.current_phase_card is not None:
            raise GameException("Player already chose the phase card this round.")
        if phase_card == self.last_phase_card:
            raise GameException("Cannot play the same phase card twice in a row.")
        self.last_phase_card = self.current_phase_card
        self.current_phase_card = phase_card
        return self.current_phase_card

    def play_project_card(self, card: ProjectCard) -> None:
        """
        Tries to play the project card.
        If successful, player will have been deducted the cost discounted for bonuses, if any.
        Player will receive all instant card bonuses, if any.

        :param card: Project card to play
        :raises GameException: if the player doesn't meet requirements for playing the card.
        """
        if not self.can_play_project_card(card):
            raise GameException(f"Requirements for playing the card {card} not met.")
        card.play(self)
        self.played_project_cards += card
        self.project_cards.remove(card)

    def can_play_project_card(self, card: ProjectCard) -> bool:
        """
        Checks whether the player meets all conditions to play the card.

        :param card: The card to test
        :return: True if player meets the conditions, False otherwise
        """
        current_phase: Phase = self.game.get_phase()
        if current_phase not in ([Phase.Development, Phase.Construction]) \
                or (current_phase.Development and card.color != CardColor.Green)\
                or (current_phase.Construction and card.color == CardColor.Green):
            return False
        return card.player_meets_conditions(self)
