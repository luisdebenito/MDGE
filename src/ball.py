import pygame
from src.help import Paintable, Movable, Position
import random
import math

PLAYER_COLOR = (255, 255, 255)
ENEMY_COLOR = (8, 55, 135)


class Ball(Paintable, Movable):
    def __init__(self, position: Position) -> None:
        self.rad: int = 10
        self.position: Position = position
        self.speed: float = 0.5
        self.color: tuple = PLAYER_COLOR
        self.outline: int = 20

    def paint(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(
            screen,
            self.color,
            (self.position.posx, self.position.posy),
            self.rad,
            self.outline,
        )

    def eat(self) -> None:
        self.rad += 10


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


class EnemyBall(Ball):
    def __init__(self, position: Position, angle: float, speed: float) -> None:
        self.rad: int = 20
        self.position: Position = position
        self.color: tuple = ENEMY_COLOR
        self.angle: float = angle
        self.angleOffset: float = random.uniform(0, math.pi / 3)
        self.speed: float = speed
        self.outline = 0

    def move(self) -> None:
        self.position.posx += math.cos(self.angle + self.angleOffset) * self.speed
        self.position.posy += math.sin(self.angle + self.angleOffset) * self.speed
