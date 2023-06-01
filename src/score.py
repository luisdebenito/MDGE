from src.help import Paintable, Movable
from src.font import score_font
import pygame

SCORE_COLOR = (159, 164, 191)


class Score(Paintable, Movable):
    def __init__(self, height: int, width: int) -> None:
        self.value = 0
        self._totalIterations = 0
        self.height = height
        self.width = width

    def paint(self, screen: pygame.Surface) -> None:
        text1 = score_font.render(str(self.value), True, SCORE_COLOR)
        text2 = score_font.render(str(self.value), True, SCORE_COLOR)
        text1.set_alpha(40)
        text2.set_alpha(40)
        textRect1 = text1.get_rect()
        textRect2 = text2.get_rect()
        textRect1.center = (self.width * 3 // 4, self.height // 2)
        textRect2.center = (self.width // 4, self.height // 2)
        screen.blit(text1, textRect1)
        screen.blit(text2, textRect2)

    def move(self) -> None:
        self._totalIterations += 1
        if self._totalIterations % 250 == 0:
            self.value += 1
