import pygame, asyncio
import sys
from typing import List, Union
from src.help import Paintable, Movable, GAMESTATUS, Position, DARK_GRAY
from src.enemySpawner import EnemySpawner
from src.ball import BallArrows, BallAWSD
from src.playground import Playground
from src.collider import Collider
from src.score import Score
from src.levelBar import LevelBar
from src.music import MusicPlayer, MUSIC_END
from src.gameOver import GameOverScreen
from src.welcomePage import WelcomePageScreen
from src.levelHandler import LevelHandler, Level
from src.levelScreen import LevelScreen


class World:
    def __init__(self) -> None:
        self._init_game()
        self._init_world()

    def _init_game(self) -> None:
        self.width: int = 800
        self.height: int = 600
        self.screen: pygame.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("M.D.G.E | Most Difficult Game Ever")
        self.gameOverScreen: GameOverScreen = GameOverScreen(
            self.screen, self.height, self.width
        )
        self.welcomePageScreen: WelcomePageScreen = WelcomePageScreen(
            self.screen, self.height, self.width
        )
        self.levelScreen: LevelScreen = LevelScreen(
            self.screen, self.height, self.width
        )
        self.musicplayer: MusicPlayer = MusicPlayer()
        self.status: GAMESTATUS = GAMESTATUS.WELCOME
        self.keys_pressed: pygame.key.ScancodeWrapper = None

    def _init_world(self) -> None:
        self.iters: int = 0
        self.gameObjects: List[Union[Movable, Paintable]] = []

        self.levelHandler: LevelHandler = LevelHandler()

        self.playground: Playground = Playground(
            Position(10, 10), self.width - 20, self.height - 20
        )
        self.levelBar: LevelBar = LevelBar(
            Position(self.width // 2, 20), self.height - 40, 60
        )
        self.score: Score = Score(self.height, self.width)
        self.enemiesSpawner: EnemySpawner = EnemySpawner(
            self.iters, self.width, self.height, self.levelHandler.getLevel()
        )
        self.playerR: BallArrows = BallArrows(
            Position(self.width * 3 // 4, self.height // 2)
        )
        self.playerL: BallAWSD = BallAWSD(Position(self.width // 4, self.height // 2))

        self.gameObjects.extend(
            [
                self.playground,
                self.levelBar,
                self.score,
                self.enemiesSpawner,
                self.playerR,
                self.playerL,
            ]
        )

    def _init_level(self) -> None:
        level: Level = self.levelHandler.getLevel()
        self.playerR.restart(Position(self.width * 3 // 4, self.height // 2))
        self.playerL.restart(Position(self.width // 4, self.height // 2))
        self.enemiesSpawner.restart(self.iters, level)
        self.levelBar.restart()
        self.levelBar.set_level(level.number)
        self.score.value = self.levelHandler.lifes
        self.status = GAMESTATUS.PLAYING

    async def play(self) -> None:
        while True:
            self.iters += 1
            self.handle_events()
            if self.status == GAMESTATUS.PLAYING:
                self._playing()
                continue

            if self.status == GAMESTATUS.LEVELOVER:
                self._checkSpaceBar(False)
                self.levelScreen.show(
                    "··· You died ···",
                    self.levelHandler.getLevel().number,
                    self.levelHandler.lifes,
                    self.playerL,
                    self.playerR,
                )
                continue

            if self.status == GAMESTATUS.LEVELUP:
                self._checkSpaceBar(False)
                num = self.levelHandler.getLevel().number
                self.levelScreen.show(
                    f"··· Level {num-1} completed ··· +1Life",
                    num,
                    self.levelHandler.lifes,
                    self.playerL,
                    self.playerR,
                )
                continue

            self._checkSpaceBar()
            if self.status == GAMESTATUS.GAMEDONE:
                self.gameOverScreen.show(
                    f"SCORE {self.levelHandler.lifes}",
                    self.playerL,
                    self.playerR,
                    "YOU WON",
                )
                continue

            if self.status == GAMESTATUS.GAMEOVER:
                self.gameOverScreen.show(
                    f"LEVEL {self.levelHandler.getLevel().number}",
                    self.playerL,
                    self.playerR,
                    "GAME OVER",
                )
                continue

            self.welcomePageScreen.show()

            await asyncio.sleep(0)

    def handle_events(self) -> None:
        self.keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit()
            if event.type == MUSIC_END:
                self.musicplayer.play()

    def _playing(self) -> None:
        self.enemiesSpawner.spawnEnemies(self.iters)
        self.move()
        self.calculateColliders()
        self.enemiesSpawner.update_grid_size(
            max(self.playerL.rad, self.playerR.rad) + 20
        )
        self.checkLevelStatus()
        self.paint()

    def checkLevelStatus(self) -> None:
        if not self.levelBar.is_completed():
            return
        self.levelHandler.levelUp()
        if not self.levelHandler.getLevel():
            self.status = GAMESTATUS.GAMEDONE
            self.musicplayer.stop()
            return
        self.musicplayer.pauseUnpause()
        self.status = GAMESTATUS.LEVELUP

    def move(self) -> None:
        for gameObject in self.gameObjects:
            if isinstance(gameObject, Movable):
                gameObject.move(self.keys_pressed)

    def paint(self) -> None:
        self.screen.fill(DARK_GRAY)
        for gameObject in self.gameObjects:
            if isinstance(gameObject, Paintable):
                gameObject.paint(self.screen)
        pygame.display.flip()

    def calculateColliders(self) -> None:
        if any(
            [
                Collider.checkLeftBall_w_Playground(self.playerL, self.playground),
                Collider.checkRightBall_w_Playground(self.playerR, self.playground),
            ]
        ):
            self.levelHandler.kill()
            if self.levelHandler.is_dead():
                self.status = GAMESTATUS.GAMEOVER
                self.musicplayer.stop()
            else:
                self.status = GAMESTATUS.LEVELOVER
                self.musicplayer.pauseUnpause()

        for ball in [self.playerL, self.playerR]:
            if enemy := Collider.check_Ball_w_Enemies(ball, self.enemiesSpawner):
                ball.eat()
                self.enemiesSpawner.removeEnemy(enemy)

    def _checkSpaceBar(self, world: bool = True) -> None:
        if self.keys_pressed[pygame.K_SPACE]:
            if world:
                self._init_world()
                self.musicplayer.play()
            else:
                self.musicplayer.pauseUnpause()
            self._init_level()
            self.status = GAMESTATUS.PLAYING

    def _exit(self) -> None:
        pygame.quit()
        sys.exit()
