from src.help import Paintable, Movable, Position, SPEED_RATIO
from src.font import energybar_font
from src.messages import Messages
import pygame

ENERGY_COLOR: tuple = (147, 183, 190)


class LevelBar(Paintable, Movable):
    paintedHeight: int = 0

    def __init__(self, position: Position, height: int, width: int) -> None:
        self.position: Position = position
        self.height: int = height
        self.width: int = width

        self.position.posx = self.position.posx - self.width // 2
        self.msg = Messages.score()

    def paint(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            ENERGY_COLOR,
            (
                self.position.posx,
                self.position.posy + self.height - self.paintedHeight + 1,
                self.width,
                self.paintedHeight,
            ),
        )

        for i in range(20):
            msg = self.msg[i] if len(self.msg) > i else "Empty"
            rotated_text = energybar_font.render(msg, True, ENERGY_COLOR)
            rtr = rotated_text.get_rect()
            rtr.center = (
                self.position.posx + self.width // 2,
                self.position.posy + 20 + (i * self.height // 10),
            )
            screen.blit(rotated_text, rtr)

    def move(self, keys: pygame.key.ScancodeWrapper | None = None):
        if self.paintedHeight >= self.height:
            return
        self.paintedHeight += (self.height / 50) * 0.004 * SPEED_RATIO

    def restart(self) -> None:
        self.paintedHeight = 0

    def is_completed(self) -> bool:
        return self.paintedHeight >= self.height
