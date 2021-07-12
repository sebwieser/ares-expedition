from game import Turn


class GameState:
    def __init__(self, turn: Turn):
        self.turn = turn
        self.is_game_finished: bool = False
        self.is_final_phase: bool = False
