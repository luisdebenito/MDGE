import pygame, asyncio
import sys
from typing import List
from src.help import Paintable, Movable, GAMESTATUS, Position, DARK_GRAY
from src.enemySpawner import EnemySpawner
from src.ball import BallArrows, BallAWSD
from src.playground import Playground
from src.collider import Collider
from src.score import Score
from src.energyBar import EnergyBar

from src.music import MusicPlayer

from src.gameOver import GameOverScreen
from src.welcomePage import WelcomePageScreen


class World:
    def __init__(self) -> None:
        self._init_game()
        self._init_world()

    def _init_game(self) -> None:
        self.width: int = 800
        self.height: int = 600
        self.screen: pygame.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("M.D.G.E")

        # different screens
        self.gameOverScreen: GameOverScreen = GameOverScreen(
            self.screen, self.height, self.width
        )
        self.welcomePageScreen: WelcomePageScreen = WelcomePageScreen(
            self.screen, self.height, self.width
        )

        self.musicplayer: MusicPlayer = MusicPlayer()

        # set initial status
        self.status: GAMESTATUS = GAMESTATUS.WELCOME

        # keypressed event stored in a variable
        self.keys_pressed: pygame.key.ScancodeWrapper = None

    def _init_world(self) -> None:
        self.movablePool: List[Movable] = []
        self.paintablePool: List[Paintable] = []

        # PLAYGROUND
        self.playground: Playground = Playground(
            Position(10, 10), self.width - 20, self.height - 20
        )
        self.paintablePool.append(self.playground)

        # energy bar
        self.energyBar: EnergyBar = EnergyBar(
            Position(self.width // 2, 30), self.height - 80, 40
        )
        self.paintablePool.append(self.energyBar)
        self.movablePool.append(self.energyBar)

        # SCORE
        self.score: Score = Score(self.height, self.width)
        self.paintablePool.append(self.score)
        self.movablePool.append(self.score)

        # PLAYERS
        self._declarePlayers()

        # ENEMIES
        self.enemiesSpawner: EnemySpawner = EnemySpawner(
            self.score.value, self.width, self.height
        )
        self.paintablePool.append(self.enemiesSpawner)
        self.movablePool.append(self.enemiesSpawner)

    def _declarePlayers(self) -> None:
        self.playerR: BallArrows = BallArrows(
            Position(self.width * 3 // 4, self.height // 2)
        )
        self.playerL: BallAWSD = BallAWSD(Position(self.width // 4, self.height // 2))

        self.movablePool.append(self.playerR)
        self.movablePool.append(self.playerL)

        self.paintablePool.append(self.playerR)
        self.paintablePool.append(self.playerL)

    async def play(self) -> None:
        while True:
            self.handle_events()
            if self.status == GAMESTATUS.PLAYING:
                self._playing()
            else:
                self._checkSpaceBar()
                if self.status == GAMESTATUS.GAMEOVER:
                    self.gameOverScreen.show(
                        self.score.value, self.playerL, self.playerR
                    )
                elif self.status == GAMESTATUS.WELCOME:
                    self.welcomePageScreen.show()
            await asyncio.sleep(0)

    def handle_events(self) -> None:
        self.keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit()

    def _playing(self) -> None:
        self.enemiesSpawner.spawnEnemies(self.score.value)
        self.move()
        self.calculateColliders()
        self.enemiesSpawner.update_grid_size(
            max(self.playerL.rad, self.playerR.rad) + 20
        )

        self.paint()

    def move(self) -> None:
        for movItem in self.movablePool:
            movItem.move(self.keys_pressed)

    def paint(self) -> None:
        self.screen.fill(DARK_GRAY)
        for paintItem in self.paintablePool:
            paintItem.paint(self.screen)

        pygame.display.flip()

    def calculateColliders(self) -> None:
        if any(
            [
                Collider.checkLeftBall_w_Playground(self.playerL, self.playground),
                Collider.checkRightBall_w_Playground(self.playerR, self.playground),
            ]
        ):
            self.status = GAMESTATUS.GAMEOVER
            self.musicplayer.stop()

        for ball in [self.playerL, self.playerR]:
            if enemy := Collider.check_Ball_w_Enemies(ball, self.enemiesSpawner):
                ball.eat()
                self.enemiesSpawner.removeEnemy(enemy)

    def _checkSpaceBar(self) -> None:
        if self.keys_pressed[pygame.K_SPACE]:
            self._init_world()
            self.status = GAMESTATUS.PLAYING
            # start music
            self.musicplayer.play()

    def _exit(self) -> None:
        pygame.quit()
        sys.exit()
