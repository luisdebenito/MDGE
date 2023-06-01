import pygame
from src.help import Paintable, Position

LINE_COLOR = (209, 51, 212)


class Playground(Paintable):
    def __init__(self, position: Position, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.position: Position = position

    def paint(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            LINE_COLOR,
            (
                self.position.posx,
                self.position.posy,
                self.width,
                self.height,
            ),
            5,
        )

        wall_width = 5
        wall_x = self.width // 2 - wall_width // 2
        pygame.draw.rect(
            screen,
            LINE_COLOR,
            (
                wall_x,
                10,
                wall_width,
                self.height,
            ),
        )
