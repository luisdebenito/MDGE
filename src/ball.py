import pygame
from src.help import Paintable, Movable, Position
import random
import math


class Ball(Paintable, Movable):
    def __init__(self, position: Position, color: tuple) -> None:
        self.rad: int = 10
        self.position: Position = position
        self.speed: float = 0.5
        self.color: tuple = color

    def paint(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(
            screen, self.color, (self.position.posx, self.position.posy), self.rad
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
        self.color: tuple = (40, 40, 140, 20)
        self.angle: float = angle
        self.angleOffset: float = random.uniform(0, math.pi / 3)
        self.speed: float = speed

    def move(self) -> None:
        self.position.posx += math.cos(self.angle + self.angleOffset) * self.speed
        self.position.posy += math.sin(self.angle + self.angleOffset) * self.speed
