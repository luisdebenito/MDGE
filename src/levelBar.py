from src.help import Paintable, Movable, Position, SPEED_RATIO
from src.font import energybar_font
import pygame

ENERGY_COLOR: tuple = (147, 183, 190)


class LevelBar(Paintable, Movable):
    paintedHeight: int = 0

    def __init__(self, position: Position, height: int, width: int) -> None:
        self.position: Position = position
        self.height: int = height
        self.width: int = width

        self.level: int = 0

        self.position.posx = self.position.posx - self.width // 2

    def paint(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            ENERGY_COLOR,
            (
                self.position.posx,
                self.position.posy,
                self.width,
                self.paintedHeight,
            ),
        )

        rotated_text = energybar_font.render(f"LVL {self.level}", True, ENERGY_COLOR)

        rtr = rotated_text.get_rect()
        for i in range(10):
            rtr.center = (
                self.position.posx + self.width // 2,
                self.position.posy + 20 + (i * self.height // 10),
            )
            screen.blit(rotated_text, rtr)

    def move(self, keys: pygame.key.ScancodeWrapper | None = None):
        if self.paintedHeight >= self.height:
            return
        self.paintedHeight += (self.height / 50) * 0.004 * SPEED_RATIO

    def set_level(self, level) -> None:
        self.level = level

    def restart(self) -> None:
        self.paintedHeight = 0

    def is_completed(self) -> bool:
        return self.paintedHeight >= self.height
