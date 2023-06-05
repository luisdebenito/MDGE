from abc import abstractmethod
from enum import Enum
import pygame
import os

SPEED_RATIO = os.environ.get("SPEED_RATIO", 1)


DARK_GRAY: tuple = (40, 40, 40)
FONT_COLOR = (196, 201, 89)


class GAMESTATUS(Enum):
    WELCOME = 0
    PLAYING = 1
    GAMEOVER = 2


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
