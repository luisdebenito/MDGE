from typing import List

import pygame
from src.help import Paintable, Position


class Trail(Paintable):
    def __init__(self, color: tuple, length: int, outline: int) -> None:
        self.color: tuple = color
        self.length: int = length
        self.trailPoints: List[Position] = []
        self.outline: int = outline

    def addPoint(self, point: Position) -> None:
        self.trailPoints.append(point)
        if len(self.trailPoints) > self.length:
            self.trailPoints.pop(0)

    def paint(self, screen: pygame.Surface, width: int) -> None:
        for point in self.trailPoints:
            pygame.draw.circle(
                screen, self.color, (point.posx, point.posy), width, self.outline
            )
