import pygame
from src.help import Paintable, Movable, GAMESTATUS, Position, WHITE, DARK_GRAY
from typing import List
from src.enemySpawner import EnemySpawner
from src.ball import BallArrows, BallAWSD
from src.playground import Playground
from src.collider import Collider
import sys


class World:
    def __init__(self) -> None:
        self._init_game()
        self._init_world()

    def _init_game(self) -> None:
        self.width: int = 800
        self.height: int = 600
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.status = GAMESTATUS.GAMEOVER
        self.font = pygame.font.Font("freesansbold.ttf", 72)

    def _init_world(self) -> None:
        self.score = 0
        self._totalIters = 0
        self.movablePool: List[Movable] = []
        self.paintablePool: List[Paintable] = []

        self.playground: Playground = Playground(
            Position(10, 10), self.width - 20, self.height - 20
        )
        self.paintablePool.append(self.playground)

        self._declareBalls()

        self.enemiesSpawner: EnemySpawner = EnemySpawner(
            self.score, self.width, self.height
        )
        self.paintablePool.append(self.enemiesSpawner)
        self.movablePool.append(self.enemiesSpawner)

    def _declareBalls(self) -> None:
        self.playerR: BallArrows = BallArrows(
            Position(self.width * 3 // 4, self.height // 2), WHITE
        )
        self.playerL: BallAWSD = BallAWSD(
            Position(self.width // 4, self.height // 2), WHITE
        )

        self.movablePool.append(self.playerR)
        self.movablePool.append(self.playerL)

        self.paintablePool.append(self.playerR)
        self.paintablePool.append(self.playerL)

    def play(self) -> None:
        while True:
            self.handle_events()
            if self.status == GAMESTATUS.PLAYING:
                self.enemiesSpawner.spawnEnemies(self.score)
                self.move()
                self.calculateColliders()
                self.enemiesSpawner.update_grid_size(
                    max(self.playerL.rad, self.playerR.rad) + 20
                )
                self.scoreUp()
            elif self.status == GAMESTATUS.GAMEOVER:
                self.handleGameOver()

            self.paint()

    def scoreUp(self):
        self._totalIters += 1
        if self._totalIters % 250 == 0:
            self.score += 1

    def handleGameOver(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self._init_world()
            self.status = GAMESTATUS.PLAYING

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

    def paint(self) -> None:
        self.screen.fill(DARK_GRAY)
        self._paintScore()
        for paintItem in self.paintablePool:
            paintItem.paint(self.screen)

        pygame.display.flip()

    def _paintScore(self) -> None:
        text1 = self.font.render(str(self.score), True, (42, 56, 170, 20))
        text2 = self.font.render(str(self.score), True, (150, 26, 60, 20))
        textRect1 = text1.get_rect()
        textRect2 = text2.get_rect()
        textRect1.center = (self.width * 3 // 4, self.height // 2)
        textRect2.center = (self.width // 4, self.height // 2)
        self.screen.blit(text1, textRect1)
        self.screen.blit(text2, textRect2)
