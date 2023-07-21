from src.help import Paintable, Movable, Position
from src.ball import EnemyBall
import random
import math
import pygame
from typing import List, Optional


class EnemySpawner(Paintable, Movable):
    grid_size: int = 50
    numEnemies: int = 30

    def __init__(self, score: int, width: int, height: int) -> None:
        self.enemies: List[EnemyBall] = []
        self.height = height
        self.width = width
        self.spawn_radius = max(width, height) * 0.55
        self.grid = {}

    def update_grid_size(self, rad: int) -> None:
        self.grid_size = rad

    def spawnEnemies(self) -> None:
        self._remove_old()
        if len(self.enemies) == self.numEnemies:
            return
        self._spawn_new()

    def _spawn_new(self) -> None:
        num_balls = abs(len(self.enemies) - self.numEnemies)
        self.enemies.extend(
            [
                EnemyBall(
                    Position(
                        self.width // 2 + math.cos(angle) * self.spawn_radius,
                        self.height // 2 + math.sin(angle) * self.spawn_radius,
                    ),
                    angle,
                    speed,
                )
                for _ in range(num_balls)
                for angle, speed in [
                    (random.uniform(0, 2 * math.pi), random.uniform(0.2, 0.4) * -1)
                ]
            ]
        )
        if x := len(self.enemies) > self.numEnemies:
            self.enemies = self.enemies[: (self.numEnemies - x)]

    def _remove_old(self) -> None:
        if not self.enemies:
            return
        spawn_radius_plus_enemies_rad = self.spawn_radius + max(
            enemy.rad for enemy in self.enemies
        )
        center_x = self.width // 2
        center_y = self.height // 2
        self.enemies = [
            enemy
            for enemy in self.enemies
            if math.hypot(
                enemy.position.posx - center_x, enemy.position.posy - center_y
            )
            <= spawn_radius_plus_enemies_rad
        ]

    def removeEnemy(self, enemy: EnemyBall) -> None:
        self.enemies.remove(enemy)

    def paint(self, screen: pygame.Surface) -> None:
        for enemy in self.enemies:
            enemy.paint(screen)

    def move(self, keys: Optional[pygame.key.ScancodeWrapper] = None) -> None:
        for enemy in self.enemies:
            enemy.move()
        self.update_grid()

    def update_grid(self) -> None:
        self.grid.clear()
        for enemy in self.enemies:
            cell_x = int(enemy.position.posx // self.grid_size)
            cell_y = int(enemy.position.posy // self.grid_size)
            cell_key = (cell_x, cell_y)
            self.grid.setdefault(cell_key, []).append(enemy)
