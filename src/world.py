import pygame, asyncio
import sys
from typing import List, Union
from src.help import Paintable, Movable, GAMESTATUS, Position, DARK_GRAY, SPEED_RATIO
from src.enemySpawner import EnemySpawner
from src.ball import BallArrows, BallAWSD, PlayerBall
from src.playground import Playground
from src.collider import Collider
from src.score import Score
from src.music import MusicPlayer
from src.gameOver import GameOverScreen
from src.welcomePage import WelcomePageScreen
from ai.ai import AI, Action


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
        self.musicplayer: MusicPlayer = MusicPlayer()
        self.status: GAMESTATUS = GAMESTATUS.WELCOME
        self.keys_pressed: pygame.key.ScancodeWrapper = None

        # ai implementation
        self.ai = AI()

    def _init_world(self) -> None:
        self.gameObjects: List[Union[Movable, Paintable]] = []

        self.playground: Playground = Playground(
            Position(10, 10), self.width - 20, self.height - 20
        )

        self.score: Score = Score(self.height, self.width)
        self.enemiesSpawner: EnemySpawner = EnemySpawner(
            self.score.value, self.width, self.height
        )
        self.enemiesSpawner.maxNumEnemies = 28
        self.playerR: BallArrows = BallArrows(
            Position(self.width * 3 // 4, self.height // 2)
        )
        self.playerL: BallAWSD = BallAWSD(Position(self.width // 4, self.height // 2))

        self.gameObjects.extend(
            [
                self.playground,
                self.score,
                self.enemiesSpawner,
                self.playerR,
                self.playerL,
            ]
        )

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

        # let AI move the balls
        self.AImove()

        self.calculateColliders()
        self.enemiesSpawner.update_grid_size(
            max(self.playerL.rad, self.playerR.rad) + 20
        )

        self.paint()

    def AImove(self) -> None:
        actions: Action = self.ai._get_GameAction(
            self.playerR,
            self.playerL,
            self.enemiesSpawner.enemies,
            self.score._totalIterations,
        )
        self.playerL.move(actions.movLeft)
        self.playerR.move(actions.movRight)

    def move(self) -> None:
        for gameObject in self.gameObjects:
            if isinstance(gameObject, Movable) and not isinstance(
                gameObject, PlayerBall
            ):
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
            self.status = GAMESTATUS.GAMEOVER
            self.musicplayer.stop()

        for ball in [self.playerL, self.playerR]:
            if enemy := Collider.check_Ball_w_Enemies(ball, self.enemiesSpawner):
                ball.eat()
                self.enemiesSpawner.removeEnemy(enemy)

    def _checkSpaceBar(self) -> None:
        if self.status == GAMESTATUS.GAMEOVER:
            # Update the AI network
            self.ai.update_network()
            self._init_world()
            self.status = GAMESTATUS.PLAYING
            return
        if self.keys_pressed[pygame.K_SPACE]:
            self._init_world()
            self.status = GAMESTATUS.PLAYING
            self.musicplayer.play()

    def _exit(self) -> None:
        pygame.quit()
        sys.exit()
