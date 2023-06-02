import pygame
from src.help import DARK_GRAY, GAMEOVER_COLOR
from src.font import welcomePage_font


class WelcomePageScreen:
    def __init__(self, screen: pygame.Surface, height: int, width: int) -> None:
        self.screen: pygame.Surface = screen
        self.height: int = height
        self.width: int = width

    def show(self) -> None:
        self.screen.fill(DARK_GRAY)
        t1 = welcomePage_font.render("SPACE", True, GAMEOVER_COLOR)
        t2 = welcomePage_font.render("TO START", True, GAMEOVER_COLOR)
        tr1 = t1.get_rect()
        tr2 = t2.get_rect()
        tr1.center = (self.width // 2, self.height * 3 // 8)
        tr2.center = (self.width // 2, self.height * 5 // 8)
        self.screen.blit(t1, tr1)
        self.screen.blit(t2, tr2)
        pygame.display.flip()
