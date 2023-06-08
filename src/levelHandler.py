from typing import List


class Level:
    def __init__(
        self, number: int, maxNumEnemies: int, minNumRand: int, maxNumRand: int
    ) -> None:
        self.maxNumEnemies: int = maxNumEnemies
        self.minNumRand: int = minNumRand
        self.maxNumRand: int = maxNumRand
        self.number: int = number


class LevelHandler:
    _levels: List[Level] = [
        Level(1, 10, 3, 5),
        Level(2, 13, 3, 6),
        Level(3, 16, 4, 7),
        Level(4, 19, 5, 8),
        Level(5, 22, 6, 9),
        Level(6, 25, 7, 10),
        Level(7, 28, 8, 11),
        Level(8, 32, 9, 12),
        Level(9, 35, 10, 13),
        Level(10, 40, 11, 15),
    ]

    def __init__(self) -> None:
        self.currentLevel = 0
        self.lifes: int = 3

    def levelUp(self) -> None:
        self.currentLevel += 1
        self.lifes += 1

    def kill(self) -> None:
        self.lifes -= 1

    def is_dead(self) -> bool:
        return self.lifes <= 0

    def getLevel(self) -> Level | None:
        return (
            self._levels[self.currentLevel]
            if self.currentLevel <= (len(self._levels) - 1)
            else None
        )
