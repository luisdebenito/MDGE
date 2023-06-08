import pygame
from src.help import DARK_GRAY, YELLOW_TAXI, WHITE_LIGHT
from src.font import (
    level_big_font,
    level_small_font,
    instructions_font,
    level_medium_font,
)
from src.ball import Ball


class LevelScreen:
    def __init__(self, screen: pygame.Surface, height: int, width: int) -> None:
        self.screen: pygame.Surface = screen
        self.height: int = height
        self.width: int = width

    def show(
        self, msg: str, levelNumber: int, lifes: int, playerL: Ball, playerR: Ball
    ) -> None:
        self.screen.fill(DARK_GRAY)
        playerL.paint(self.screen)
        playerR.paint(self.screen)

        instructions = instructions_font.render("SPACE TO PLAY", True, YELLOW_TAXI)
        t0 = level_big_font.render(msg, True, YELLOW_TAXI)
        t1 = level_medium_font.render(f"Level {levelNumber}", True, YELLOW_TAXI)
        t11 = level_small_font.render(f"x {lifes}", True, YELLOW_TAXI)
        tr0 = t0.get_rect()
        tr1 = t1.get_rect()
        tr11 = t11.get_rect()
        trins = instructions.get_rect()
        tr0.center = (self.width // 2, self.height * 2 // 8)
        tr1.center = (self.width // 2, self.height * 4 // 8)
        tr11.center = ((self.width // 2) + 30, self.height * 6 // 8)
        trins.center = (self.width // 2, self.height * 1 // 12)
        self.screen.blit(t0, tr0)
        self.screen.blit(t1, tr1)
        self.screen.blit(t11, tr11)
        self.screen.blit(instructions, trins)

        pygame.draw.circle(
            self.screen,
            WHITE_LIGHT,
            ((self.width // 2) - 30, self.height * 6 // 8),
            25,
            5,
        )

        pygame.display.flip()
