import pygame
import sys
from typing import List, Union
from src.help import Paintable, Movable, GAMESTATUS, Position, DARK_GRAY
from src.enemySpawner import EnemySpawner
from src.ball import PlayerBall
from src.playground import Playground
from src.collider import Collider
from src.score import Score
from src.welcomePage import WelcomePageScreen


class World:
    def __init__(self) -> None:
        self._init_game()
        self._init_world()

    def _init_game(self) -> None:
        self.width: int = 800
        self.height: int = 600
        self.screen: pygame.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("M.D.G.E | Most Difficult Game Ever")
        self.welcomePageScreen: WelcomePageScreen = WelcomePageScreen(
            self.screen, self.height, self.width
        )
        self.status: GAMESTATUS = GAMESTATUS.WELCOME
        self.keys_pressed: pygame.key.ScancodeWrapper = None

        # ai implementation
        # self.ai = AI()

    def _init_world(self) -> None:
        self.gameObjects: List[Union[Movable, Paintable]] = []

        self.playground: Playground = Playground(
            Position(100, 50), self.width - 200, self.height - 100
        )

        self.score: Score = Score(self.height, self.width)
        self.enemiesSpawner: EnemySpawner = EnemySpawner(
            self.score.value, self.width, self.height
        )
        self.enemiesSpawner.maxNumEnemies = 28
        self.player: PlayerBall = PlayerBall(
            Position(self.width // 2, self.height // 2)
        )

        self.gameObjects.extend(
            [
                self.playground,
                self.score,
                self.enemiesSpawner,
                self.player,
            ]
        )

    def play(self) -> None:
        while True:
            self.handle_events()
            if self.status == GAMESTATUS.PLAYING:
                self._playing()
            else:
                if self.status == GAMESTATUS.GAMEOVER:
                    # self.ai.update_network()
                    self._init_world()
                    self.status = GAMESTATUS.PLAYING
                elif self.status == GAMESTATUS.WELCOME:
                    self._checkSpaceBar()
                    self.welcomePageScreen.show()

    def handle_events(self) -> None:
        self.keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit()

    def _playing(self) -> None:
        self.enemiesSpawner.spawnEnemies()
        self.move()

        # let AI move the balls
        # self.AImove()

        self.calculateColliders()
        self.enemiesSpawner.update_grid_size(self.player.rad + 20)

        self.paint()

    # def AImove(self) -> None:
    # actions: Action = self.ai._get_GameAction(
    #     self.playerR,
    #     self.playerL,
    #     self.enemiesSpawner.enemies,
    #     self.score._totalIterations,
    # )
    # self.playerL.move(actions.movLeft)
    # self.playerR.move(actions.movRight)

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
                Collider.checkBall_w_Playground(self.player, self.playground),
            ]
        ):
            self.status = GAMESTATUS.GAMEOVER

        if enemy := Collider.check_Ball_w_Enemies(self.player, self.enemiesSpawner):
            self.player.eat()
            self.enemiesSpawner.removeEnemy(enemy)

    def _checkSpaceBar(self) -> None:
        if self.keys_pressed[pygame.K_SPACE]:
            self._init_world()
            self.status = GAMESTATUS.PLAYING

    def _exit(self) -> None:
        pygame.quit()
        sys.exit()
