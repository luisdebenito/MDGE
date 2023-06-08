import pygame
from src.help import Paintable, Movable, Position, SPEED_RATIO, WHITE_LIGHT, PINK
import random
import math


class Ball(Paintable, Movable):
    speed: float = 0.55 * SPEED_RATIO
    rad: int = 10
    outline: int = 20
    color: tuple = WHITE_LIGHT

    def __init__(self, position: Position) -> None:
        self.position: Position = position

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


class PlayerBall(Ball):
    key_left: str = ""
    key_right: str = ""
    key_up: str = ""
    key_down: str = ""

    def move(self, keys: pygame.key.ScancodeWrapper) -> None:
        # Determine the movement direction based on the pressed keys
        dx = (keys[self.key_right] != 0) - (keys[self.key_left] != 0)
        dy = (keys[self.key_down] != 0) - (keys[self.key_up] != 0)

        # Calculate the diagonal movement factor
        diagonal_factor = 1 / math.sqrt(2) if dx != 0 and dy != 0 else 1

        # Update the position based on the direction and speed
        self.position.posx += dx * self.speed * diagonal_factor
        self.position.posy += dy * self.speed * diagonal_factor

    def restart(self, position: Position):
        self.rad = 10
        self.position = position


class BallArrows(PlayerBall):
    key_down = pygame.K_DOWN
    key_left = pygame.K_LEFT
    key_right = pygame.K_RIGHT
    key_up = pygame.K_UP


class BallAWSD(PlayerBall):
    key_down = pygame.K_s
    key_left = pygame.K_a
    key_right = pygame.K_d
    key_up = pygame.K_w


class EnemyBall(Ball):
    rad: int = 20
    color: tuple = PINK
    outline: int = 0

    def __init__(self, position: Position, angle: float, speed: float) -> None:
        super().__init__(position)
        self.angle: float = angle
        self.angleOffset: float = random.uniform(0, math.pi / 3)
        self.speed: float = speed * SPEED_RATIO

    def move(self) -> None:
        self.position.posx += math.cos(self.angle + self.angleOffset) * self.speed
        self.position.posy += math.sin(self.angle + self.angleOffset) * self.speed
