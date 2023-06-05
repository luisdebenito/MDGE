import pygame
from src.help import DARK_GRAY, FONT_COLOR
from src.font import welcomePage_font, instructions_font


class WelcomePageScreen:
    def __init__(self, screen: pygame.Surface, height: int, width: int) -> None:
        self.screen: pygame.Surface = screen
        self.height: int = height
        self.width: int = width

    def show(self) -> None:
        self.screen.fill(DARK_GRAY)
        t1 = welcomePage_font.render("SPACE", True, FONT_COLOR)
        t2 = welcomePage_font.render("TO PLAY", True, FONT_COLOR)

        t3 = instructions_font.render("ARROWS right ball", True, FONT_COLOR)
        t4 = instructions_font.render("ASDW left ball", True, FONT_COLOR)
        tr1 = t1.get_rect()
        tr2 = t2.get_rect()
        tr3 = t3.get_rect()
        tr4 = t3.get_rect()
        tr1.center = (self.width // 2, self.height * 3 // 8)
        tr2.center = (self.width // 2, self.height * 5 // 8)
        tr3.center = (self.width // 2, self.height * 7 // 8)
        tr4.center = (self.width // 2, self.height * 7.5 // 8)
        self.screen.blit(t1, tr1)
        self.screen.blit(t2, tr2)
        self.screen.blit(t3, tr3)
        self.screen.blit(t4, tr4)
        pygame.display.flip()
