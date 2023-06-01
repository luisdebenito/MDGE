import pygame
from src.help import Paintable, Movable, GAMESTATUS, Position, DARK_GRAY
from typing import List
from src.enemySpawner import EnemySpawner
from src.ball import BallArrows, BallAWSD
from src.playground import Playground
from src.collider import Collider
from src.score import Score
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
                self.enemiesSpawner.spawnEnemies(self.score.value)
                self.move()
                self.calculateColliders()
                self.enemiesSpawner.update_grid_size(
                    max(self.playerL.rad, self.playerR.rad) + 20
                )
            elif self.status == GAMESTATUS.GAMEOVER:
                self.handleGameOver()

            self.paint()

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
        for paintItem in self.paintablePool:
            paintItem.paint(self.screen)

        pygame.display.flip()
