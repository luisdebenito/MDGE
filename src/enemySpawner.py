from src.help import Paintable, Movable, Position, SPEED_RATIO
from src.ball import EnemyBall
from src.levelHandler import Level
import random
import math
import pygame
from typing import List, Optional


class EnemySpawner(Paintable, Movable):
    grid_size: int = 50

    def __init__(self, iter: int, width: int, height: int, level: Level) -> None:
        self.height = height
        self.width = width
        self.spawn_radius = max(width, height) * 0.55
        self.next_spawn_delay = 250 // SPEED_RATIO
        self.restart(iter, level)

    def restart(self, iter: int, level: Level) -> None:
        self.enemies: List[EnemyBall] = []
        self.grid = {}

        self.maxNumEnemies: int = level.maxNumEnemies
        self.minNumRand: int = level.minNumRand
        self.maxNumRand: int = level.maxNumRand
        self._generate_next_spawn_delay(iter)

    def update_grid_size(self, rad: int) -> None:
        self.grid_size = rad

    def _generate_next_spawn_delay(self, iter: int) -> None:
        self.last_spawn_time = iter

    def spawnEnemies(self, iter: int) -> None:
        self._remove_old()
        if (
            len(self.enemies) >= self.maxNumEnemies
            or iter - self.last_spawn_time < self.next_spawn_delay
        ):
            return
        self._spawn_new(iter)

    def _spawn_new(self, iter: int) -> None:
        num_balls = random.randint(self.minNumRand, self.maxNumRand)
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
                    (random.uniform(0, 2 * math.pi), random.uniform(0.3, 0.6) * -1)
                ]
            ]
        )
        self._generate_next_spawn_delay(iter)

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
