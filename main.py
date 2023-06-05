import pygame, asyncio

pygame.init()
pygame.mouse.set_visible(False)

from src.world import World

world = World()


async def main():
    await world.play()


asyncio.run(main())
