from abc import abstractmethod
import pygame
import sys


BLACK: tuple = (20, 20, 20)
DARK_GRAY: tuple = (40, 40, 40)
WHITE: tuple = (255, 255, 255)


class Position:
    def __init__(self, posx: int, posy: int) -> None:
        self.posx: int = posx
        self.posy: int = posy


class Ball:
    def __init__(self, position: Position, color: tuple) -> None:
        self.rad: int = 10
        self.position: Position = position
        self.speed: float = 0.5
        self.color: tuple = color

    def paint(self, screen) -> None:
        pygame.draw.circle(
            screen, self.color, (self.position.posx, self.position.posy), self.rad
        )

    @abstractmethod
    def move(self, screen) -> None:
        pass


class BallArrows(Ball):
    def move(self, playground) -> None:
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
    def move(self, playground) -> None:
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


class World:
    def __init__(self) -> None:
        self.width: int = 800
        self.height: int = 600
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

        self._declareBalls()

    def _declareBalls(self) -> None:
        self.ballRight: BallArrows = BallArrows(Position(1, 1), WHITE)
        self.ballAsd: BallAWSD = BallAWSD(Position(345, 345), WHITE)

    def play(self) -> None:
        while True:
            self._handle_events()
            self._move()
            self._paint()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def _move(self) -> None:
        self.ballRight.move(None)
        self.ballAsd.move(None)

    def _paint(self) -> None:
        # Update the display
        self.screen.fill(DARK_GRAY)
        self.ballRight.paint(self.screen)
        self.ballAsd.paint(self.screen)
        pygame.draw.rect(
            self.screen,
            WHITE,
            (
                10,
                10,
                self.width - 10 * 2,
                self.height - 10 * 2,
            ),
            2,
        )
        pygame.display.flip()


world = World()

world.play()
