from abc import abstractmethod
from enum import Enum
import pygame


DARK_GRAY: tuple = (40, 40, 40)


class GAMESTATUS(Enum):
    PLAYING = 0
    GAMEOVER = 1


class Paintable:
    @abstractmethod
    def paint(self, screen: pygame.Surface) -> None:
        pass


class Movable:
    @abstractmethod
    def move(self) -> None:
        pass


class Position:
    def __init__(self, posx: int, posy: int) -> None:
        self.posx: int = posx
        self.posy: int = posy
