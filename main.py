import pygame

pygame.init()
pygame.mouse.set_visible(False)

from src.world import World

world = World()

world.play()
