import pygame
import sys
from typing import List
from src.help import Paintable, Movable, GAMESTATUS, Position, DARK_GRAY
from src.enemySpawner import EnemySpawner
from src.ball import BallArrows, BallAWSD
from src.playground import Playground
from src.collider import Collider
from src.score import Score
from src.font import gameOver_font, welcomePage_font

GAMEOVER_COLOR = (196, 201, 89)


class World:
    def __init__(self) -> None:
        self._init_game()
        self._init_world()

    def _init_game(self) -> None:
        self.width: int = 800
        self.height: int = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.status = GAMESTATUS.WELCOME

    def _init_world(self) -> None:
        self.movablePool: List[Movable] = []
        self.paintablePool: List[Paintable] = []

        # PLAYGROUND
        self.playground: Playground = Playground(
            Position(10, 10), self.width - 20, self.height - 20
        )
        self.paintablePool.append(self.playground)

        # SCORE
        self.score: Score = Score(self.height, self.width)
        self.paintablePool.append(self.score)
        self.movablePool.append(self.score)

        # PLAYERS
        self._declareBalls()

        # ENEMIES
        self.enemiesSpawner: EnemySpawner = EnemySpawner(
            self.score.value, self.width, self.height
        )
        self.paintablePool.append(self.enemiesSpawner)
        self.movablePool.append(self.enemiesSpawner)

    def _declareBalls(self) -> None:
        self.playerR: BallArrows = BallArrows(
            Position(self.width * 3 // 4, self.height // 2)
        )
        self.playerL: BallAWSD = BallAWSD(Position(self.width // 4, self.height // 2))

        self.movablePool.append(self.playerR)
        self.movablePool.append(self.playerL)

        self.paintablePool.append(self.playerR)
        self.paintablePool.append(self.playerL)

    def play(self) -> None:
        while True:
            self.handle_events()
            if self.status == GAMESTATUS.PLAYING:
                self._playing()
            elif self.status == GAMESTATUS.GAMEOVER:
                self.gameOver()
            elif self.status == GAMESTATUS.WELCOME:
                self.welcomePage()

    def _playing(self) -> None:
        self.enemiesSpawner.spawnEnemies(self.score.value)
        self.move()
        self.calculateColliders()
        self.enemiesSpawner.update_grid_size(
            max(self.playerL.rad, self.playerR.rad) + 20
        )

        self._paint_playing()

    def gameOver(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self._init_world()
            self.status = GAMESTATUS.PLAYING
        self._paint_gameOver()

    def _paint_gameOver(self) -> None:
        self.screen.fill(DARK_GRAY)
        self.playerL.paint(self.screen)
        self.playerR.paint(self.screen)

        textGO = gameOver_font.render("GAME OVER", True, GAMEOVER_COLOR)
        textSC = gameOver_font.render(str(self.score.value), True, GAMEOVER_COLOR)
        textRectGo = textGO.get_rect()
        textRectSC = textSC.get_rect()
        textRectGo.center = (self.width // 2, self.height * 3.5 // 8)
        textRectSC.center = (self.width // 2, self.height * 5.5 // 8)
        self.screen.blit(textGO, textRectGo)
        self.screen.blit(textSC, textRectSC)
        pygame.display.flip()

    def welcomePage(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self._init_world()
            self.status = GAMESTATUS.PLAYING
        self._paint_welcomePage()

    def _paint_welcomePage(self) -> None:
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

    def calculateColliders(self) -> None:
        if any(
            [
                Collider.checkLeftBall_w_Playground(self.playerL, self.playground),
                Collider.checkRightBall_w_Playground(self.playerR, self.playground),
            ]
        ):
            self.status = GAMESTATUS.GAMEOVER

        for ball in [self.playerL, self.playerR]:
            if enemy := Collider.check_Ball_w_Enemies(ball, self.enemiesSpawner):
                ball.eat()
                self.enemiesSpawner.removeEnemy(enemy)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self._exit()

    def _exit(self) -> None:
        pygame.quit()
        sys.exit()

    def move(self) -> None:
        for movItem in self.movablePool:
            movItem.move()

    def _paint_playing(self) -> None:
        self.screen.fill(DARK_GRAY)
        for paintItem in self.paintablePool:
            paintItem.paint(self.screen)

        pygame.display.flip()
