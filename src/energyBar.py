from src.help import Paintable, Movable, Position, SPEED_RATIO, DARK_GRAY
from src.font import energybar_font
import pygame

ENERGY_COLOR = (196, 201, 89)
CONSUMABLE_COLOR = (136, 252, 3)


class EnergyBar(Paintable, Movable):
    paintedHeight: int = 0

    def __init__(self, position: Position, height: int, width: int) -> None:
        self.position: Position = position
        self.height: int = height
        self.width: int = width

        self.position.posx = self.position.posx - self.width // 2

    def paint(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            CONSUMABLE_COLOR if self.is_Consumable() else ENERGY_COLOR,
            (
                self.position.posx,
                self.position.posy,
                self.width,
                self.paintedHeight,
            ),
        )
        if not self.is_Consumable():
            return

        rotated_text = pygame.transform.rotate(
            energybar_font.render("SPACE FOR REDUCTION", True, DARK_GRAY), 270
        )

        rtr = rotated_text.get_rect()
        rtr.center = (
            self.position.posx + self.width // 2,
            self.position.posy + self.height // 2,
        )
        screen.blit(rotated_text, rtr)

    def move(self, keys: pygame.key.ScancodeWrapper | None = None):
        if self.paintedHeight >= self.height:
            return
        self.paintedHeight += (self.height / 50) * 0.005 * SPEED_RATIO

    def is_Consumable(self) -> bool:
        return self.paintedHeight >= self.height

    def restart(self) -> None:
        self.paintedHeight = 0
