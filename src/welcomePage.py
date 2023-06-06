import pygame
from src.help import DARK_GRAY, YELLOW_TAXI
from src.font import welcomePage_font, instructions_font


class WelcomePageScreen:
    def __init__(self, screen: pygame.Surface, height: int, width: int) -> None:
        self.screen: pygame.Surface = screen
        self.height: int = height
        self.width: int = width

    def show(self) -> None:
        self.screen.fill(DARK_GRAY)
        t1 = welcomePage_font.render("Most", True, YELLOW_TAXI)
        t11 = welcomePage_font.render("Difficult", True, YELLOW_TAXI)
        t2 = welcomePage_font.render("Game Ever", True, YELLOW_TAXI)

        t5 = instructions_font.render("SPACE TO PLAY", True, YELLOW_TAXI)
        t3 = instructions_font.render("ARROWS right ball", True, YELLOW_TAXI)
        t4 = instructions_font.render("ASDW left ball", True, YELLOW_TAXI)
        tr1 = t1.get_rect()
        tr11 = t11.get_rect()
        tr2 = t2.get_rect()
        tr3 = t3.get_rect()
        tr4 = t3.get_rect()
        tr5 = t5.get_rect()
        tr1.center = (self.width // 2, self.height * 1 // 8)
        tr11.center = (self.width // 2, self.height * 2.5 // 8)
        tr2.center = (self.width // 2, self.height * 4 // 8)
        tr3.center = (self.width * 3 // 4, self.height * 6.5 // 8)
        tr4.center = (self.width // 4, self.height * 6.5 // 8)
        tr5.center = (self.width // 2, self.height * 5.5 // 8)
        self.screen.blit(t1, tr1)
        self.screen.blit(t11, tr11)
        self.screen.blit(t2, tr2)
        self.screen.blit(t3, tr3)
        self.screen.blit(t4, tr4)
        self.screen.blit(t5, tr5)
        pygame.display.flip()
