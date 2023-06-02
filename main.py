import pygame, asyncio

pygame.init()

from src.world import World

world = World()


async def main():
    await world.play()


asyncio.run(main())
