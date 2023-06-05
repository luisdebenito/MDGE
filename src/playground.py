import pygame
from src.help import Paintable, Position

LINE_COLOR = (209, 51, 212)
WALL_COLOR = (196, 201, 89)


class Playground(Paintable):
    wall_width: int = 80

    def __init__(self, position: Position, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.position: Position = position
        self.wall_x = (self.width // 2 - self.wall_width // 2) + self.position.posx

    def paint(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            WALL_COLOR,
            (
                self.wall_x,
                self.position.posy,
                self.wall_width,
                self.height,
            ),
            20,
        )

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
