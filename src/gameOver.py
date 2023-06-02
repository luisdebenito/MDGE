import pygame
from src.help import DARK_GRAY, GAMEOVER_COLOR
from src.music import MusicPlayer
from src.font import gameOver_font
from src.ball import Ball


class GameOverScreen:
    def __init__(self, screen: pygame.Surface, height: int, width: int) -> None:
        self.screen: pygame.Surface = screen
        self.height: int = height
        self.width: int = width

    def show(self, score: int, playerL: Ball, playerR: Ball) -> None:
        self.screen.fill(DARK_GRAY)
        playerL.paint(self.screen)
        playerR.paint(self.screen)

        textGO = gameOver_font.render("GAME OVER", True, GAMEOVER_COLOR)
        textSC = gameOver_font.render(str(score), True, GAMEOVER_COLOR)
        textRectGo = textGO.get_rect()
        textRectSC = textSC.get_rect()
        textRectGo.center = (self.width // 2, self.height * 3.5 // 8)
        textRectSC.center = (self.width // 2, self.height * 5.5 // 8)
        self.screen.blit(textGO, textRectGo)
        self.screen.blit(textSC, textRectSC)
        pygame.display.flip()
