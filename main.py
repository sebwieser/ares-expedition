from game import Game
from enums import PlayerColor
from player import Player


def main():
    p1 = Player(name="Seb", color=PlayerColor.Yellow)
    p2 = Player(name="Nela", color=PlayerColor.Green)
    g1 = Game([p1, p2], None, None)
    g1.start()


if __name__ == '__main__':
    main()
