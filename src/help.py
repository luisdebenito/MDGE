from abc import abstractmethod
from enum import Enum
import pygame
import os

SPEED_RATIO = int(os.environ.get("SPEED_RATIO", 5))


DARK_GRAY: tuple = (40, 40, 40)
YELLOW_TAXI: tuple = (196, 201, 89)
WHITE_LIGHT: tuple = (210, 210, 210)
PINK: tuple = (166, 58, 80)


class GAMESTATUS(Enum):
    WELCOME = 0
    PLAYING = 1
    LEVELOVER = 2
    LEVELUP = 3
    GAMEOVER = 4
    GAMEDONE = 5


class Paintable:
    @abstractmethod
    def paint(self, screen: pygame.Surface) -> None:
        pass


class Movable:
    @abstractmethod
    def move(self, keys: pygame.key.ScancodeWrapper | None = None) -> None:
        pass


class Position:
    def __init__(self, posx: int, posy: int) -> None:
        self.posx: int = posx
        self.posy: int = posy
