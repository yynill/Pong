import pygame
from game import PongGame


class PongAi:
    def __init__(self) -> None:
        game = PongGame(True)
        game.run_game()


if __name__ == "__main__":
    pong_ai = PongAi()
