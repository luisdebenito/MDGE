import pygame
from src.help import DARK_GRAY, YELLOW_TAXI
from src.font import gameOver_font, credit_font, instructions_font, level_big_font
from src.ball import Ball


class GameOverScreen:
    def __init__(self, screen: pygame.Surface, height: int, width: int) -> None:
        self.screen: pygame.Surface = screen
        self.height: int = height
        self.width: int = width

    def show(self, msgScore: str, playerL: Ball, playerR: Ball, msg: str) -> None:
        self.screen.fill(DARK_GRAY)
        playerL.paint(self.screen)
        playerR.paint(self.screen)

        textGO = gameOver_font.render(msg, True, YELLOW_TAXI)
        textSC = level_big_font.render(msgScore, True, YELLOW_TAXI)

        creditLuis = credit_font.render("Created by Luis de Benito | @luisbq_", True, YELLOW_TAXI)
        creditDesign = credit_font.render("Designed by Elena Alonso | @EleenaAG00", True, YELLOW_TAXI)
        creditMusic = credit_font.render(
            "Music by Luis de Benito based on 'The Thin Red Line' OST", True, YELLOW_TAXI
        )

        instructions = instructions_font.render(
            "SPACE TO PLAY AGAIN", True, YELLOW_TAXI
        )

        textRectGo = textGO.get_rect()
        textRectSC = textSC.get_rect()

        creditLuisRect = creditLuis.get_rect()
        creditDesignRect = creditDesign.get_rect()
        creditMusicRect = creditMusic.get_rect()

        instrucRect = instructions.get_rect()

        textRectGo.center = (self.width // 2, self.height * 2 // 8)
        textRectSC.center = (self.width // 2, self.height * 4 // 8)

        creditLuisRect.center = (self.width // 2, self.height * 10 // 13)
        creditDesignRect.center = (self.width // 2, self.height * 11 // 13)
        creditMusicRect.center = (self.width // 2, self.height * 12 // 13)

        instrucRect.center = (self.width // 2, self.height * 0.7 // 12)

        self.screen.blit(textGO, textRectGo)
        self.screen.blit(textSC, textRectSC)

        self.screen.blit(creditLuis, creditLuisRect)
        self.screen.blit(creditDesign, creditDesignRect)
        self.screen.blit(creditMusic, creditMusicRect)

        self.screen.blit(instructions, instrucRect)
        pygame.display.flip()
