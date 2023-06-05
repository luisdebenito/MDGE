from src.help import Paintable, Movable, Position
from src.ball import EnemyBall
import random
import math
import pygame
from typing import List


class EnemySpawner(Paintable, Movable):
    def __init__(self, score: int, width: int, height: int) -> None:
        self.enemies: List[EnemyBall] = []

        # area where the world is
        self.height = height
        self.width = width

        # spawn enemies settings
        self.maxNumEnemies: int = 27
        self.spawn_radius = max(width, height) * 0.55
        self._generate_next_spawn_delay(score)

        # collider variables
        self.grid_size = 50
        self.grid = {}

    def update_grid_size(self, rad: int) -> None:
        self.grid_size = rad

    def _generate_next_spawn_delay(self, score: int) -> None:
        self.last_spawn_time = score
        self.next_spawn_delay = 2

    def spawnEnemies(self, score: int) -> None:
        self._remove_old()
        if (len(self.enemies) >= self.maxNumEnemies) or (
            score - self.last_spawn_time < self.next_spawn_delay
        ):
            return

        self._spawn_new(score)

    def _spawn_new(self, score: int) -> None:
        num_balls = random.randint(4, 7)
        for _ in range(num_balls):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.3, 0.6) * -1

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
                self.removeEnemy(en_ball)

    def removeEnemy(self, enemy: EnemyBall):
        self.enemies.remove(enemy)

    def paint(self, screen: pygame.Surface) -> None:
        for enemy in self.enemies:
            enemy.paint(screen)

    def move(self, keys: pygame.key.ScancodeWrapper | None = None) -> None:
        for enemy in self.enemies:
            enemy.move()
        self.update_grid()

    def update_grid(self) -> None:
        self.grid.clear()
        for enemy in self.enemies:
            cell_x = int(enemy.position.posx // self.grid_size)
            cell_y = int(enemy.position.posy // self.grid_size)
            cell_key = (cell_x, cell_y)
            if cell_key not in self.grid:
                self.grid[cell_key] = []
            self.grid[cell_key].append(enemy)
