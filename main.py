from abc import abstractmethod
from typing import List
import pygame
import sys
import math
import random
from enum import Enum


BLACK: tuple = (20, 20, 20)
DARK_GRAY: tuple = (40, 40, 40)
WHITE: tuple = (255, 255, 255)


class GAMESTATUS(Enum):
    PLAYING = 0
    GAMEOVER = 1


class Paintable:
    @abstractmethod
    def paint(self, screen) -> None:
        pass


class Movable:
    @abstractmethod
    def move(self) -> None:
        pass


class Position:
    def __init__(self, posx: int, posy: int) -> None:
        self.posx: int = posx
        self.posy: int = posy


class Ball(Paintable, Movable):
    def __init__(self, position: Position, color: tuple) -> None:
        self.rad: int = 10
        self.position: Position = position
        self.speed: float = 0.5
        self.color: tuple = color

    def paint(self, screen) -> None:
        pygame.draw.circle(
            screen, self.color, (self.position.posx, self.position.posy), self.rad
        )


class BallArrows(Ball):
    def move(self) -> None:
        # Handle arrow key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.position.posy -= self.speed
        if keys[pygame.K_DOWN]:
            self.position.posy += self.speed
        if keys[pygame.K_LEFT]:
            self.position.posx -= self.speed
        if keys[pygame.K_RIGHT]:
            self.position.posx += self.speed


class BallAWSD(Ball):
    def move(self) -> None:
        # Handle arrow key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.position.posy -= self.speed
        if keys[pygame.K_s]:
            self.position.posy += self.speed
        if keys[pygame.K_a]:
            self.position.posx -= self.speed
        if keys[pygame.K_d]:
            self.position.posx += self.speed


class EnemySpawner(Paintable, Movable):
    def __init__(self, score: int, width: int, height: int) -> None:
        self.enemies: List[EnemyBall] = []
        self.height = height
        self.width = width
        self.maxNumEnemies: int = 20
        self.spawn_radius = max(width, height) * 0.55
        self._generate_next_spawn_delay(score)

    def _generate_next_spawn_delay(self, score) -> None:
        self.last_spawn_time = score
        self.next_spawn_delay = 2

    def spawnEnemies(self, score) -> None:
        self._remove_old()
        if (len(self.enemies) >= self.maxNumEnemies) or (
            score - self.last_spawn_time < self.next_spawn_delay
        ):
            return

        self._spawn_new(score)

    def _spawn_new(self, score: int) -> None:
        num_balls = random.randint(3, 7)
        for _ in range(num_balls):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.2, 0.5) * -1

            spawn_x = self.width // 2 + math.cos(angle) * self.spawn_radius
            spawn_y = self.height // 2 + math.sin(angle) * self.spawn_radius

            position = Position(spawn_x, spawn_y)
            enemy_ball = EnemyBall(position, angle, speed)

            self.enemies.append(enemy_ball)

        self._generate_next_spawn_delay(score)

    def _remove_old(self) -> None:
        for en_ball in self.enemies:
            distance = math.sqrt(
                (en_ball.position.posx - self.width // 2) ** 2
                + (en_ball.position.posy - self.height // 2) ** 2
            )
            if distance > self.spawn_radius + en_ball.rad:
                self.enemies.remove(en_ball)

    def paint(self, screen) -> None:
        for enemy in self.enemies:
            enemy.paint(screen)

    def move(self) -> None:
        for enemy in self.enemies:
            enemy.move()


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
        self.totalIters = 0
        self.movablePool: List[Movable] = []
        self.paintablePool: List[Paintable] = []

        self.playground: Playground = Playground(self.width - 15, self.height - 15)
        self.paintablePool.append(self.playground)

        self._declareBalls()

        self.enemiesSpawner: EnemySpawner = EnemySpawner(
            self.score, self.width, self.height
        )
        self.paintablePool.append(self.enemiesSpawner)
        self.movablePool.append(self.enemiesSpawner)

    def _declareBalls(self) -> None:
        self.ballRight: BallArrows = BallArrows(
            Position(self.width * 3 // 4, self.height // 2), WHITE
        )
        self.ballAsd: BallAWSD = BallAWSD(
            Position(self.width // 4, self.height // 2), WHITE
        )

        self.movablePool.append(self.ballRight)
        self.movablePool.append(self.ballAsd)

        self.paintablePool.append(self.ballRight)
        self.paintablePool.append(self.ballAsd)

    def play(self) -> None:
        while True:
            self.handle_events()
            if self.status == GAMESTATUS.PLAYING:
                self.enemiesSpawner.spawnEnemies(self.score)
                self.move()
                self.calculateColliders()
                self.scoreUp()
            elif self.status == GAMESTATUS.GAMEOVER:
                self.hangleGameOver()

            self.paint()

    def scoreUp(self):
        self.totalIters += 1
        if self.totalIters % 250 == 0:
            self.score += 1

    def hangleGameOver(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self._init_world()
            self.status = GAMESTATUS.PLAYING

    def calculateColliders(self) -> None:
        pass

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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


# set the center of the rectangular object.


class Playground(Paintable):
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height

    def paint(self, screen) -> None:
        pygame.draw.rect(
            screen,
            WHITE,
            (
                10,
                10,
                self.width,
                self.height,
            ),
            2,
        )

        wall_width = 5
        wall_x = self.width // 2 - wall_width // 2
        pygame.draw.rect(
            screen,
            WHITE,
            (
                wall_x,
                10,
                wall_width,
                self.height,
            ),
        )


class EnemyBall(Ball):
    def __init__(self, position: Position, angle: float, speed: float) -> None:
        self.rad: int = 20
        self.position: Position = position
        self.color: tuple = (40, 40, 140)
        self.angle: float = angle
        self.angleOffset: float = random.uniform(0, math.pi / 3)
        self.speed: float = speed

    def move(self) -> None:
        self.position.posx += math.cos(self.angle + self.angleOffset) * self.speed
        self.position.posy += math.sin(self.angle + self.angleOffset) * self.speed


world = World()

world.play()
