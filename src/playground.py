import pygame
from src.help import Paintable, Position, WHITE


class Playground(Paintable):
    def __init__(self, position: Position, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.position: Position = position

    def paint(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            WHITE,
            (
                self.position.posx,
                self.position.posy,
                self.width,
                self.height,
            ),
            2,
        )

        wall_width = 5
        wall_x = self.width // 2 - wall_width // 2
        pygame.draw.rect(
            screen,
            WHITE,
            (
                wall_x,
                10,
                wall_width,
                self.height,
            ),
        )
