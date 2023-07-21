import pygame
from src.help import Paintable, Position, YELLOW_TAXI


class Playground(Paintable):
    def __init__(self, position: Position, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.position: Position = position

    def paint(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            YELLOW_TAXI,
            (
                self.position.posx,
                self.position.posy,
                self.width,
                self.height,
            ),
            5,
        )
