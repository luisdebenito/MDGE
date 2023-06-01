from src.ball import BallAWSD, BallArrows, EnemyBall, Ball
from src.playground import Playground
from src.enemySpawner import EnemySpawner


class Collider:
    def checkLeftBall_w_Playground(ball: BallAWSD, pg: Playground) -> bool:
        return (
            (ball.position.posx - ball.rad < pg.position.posx)
            or (ball.position.posx + ball.rad > (pg.position.posx + pg.width) // 2)
            or ball.position.posy - ball.rad < pg.position.posy
            or ball.position.posy + ball.rad > pg.position.posy + pg.height
        )

    def checkRightBall_w_Playground(ball: BallArrows, pg: Playground) -> bool:
        return (
            ball.position.posx - ball.rad < (pg.position.posx + pg.width) // 2
            or ball.position.posx + ball.rad > pg.position.posx + pg.width
            or ball.position.posy - ball.rad < pg.position.posy
            or ball.position.posy + ball.rad > pg.position.posy + pg.height
        )

    def check_Ball_w_Enemies(
        ball: Ball, enemySpawner: EnemySpawner
    ) -> EnemyBall | bool:
        cell_x = int(ball.position.posx // enemySpawner.grid_size)
        cell_y = int(ball.position.posy // enemySpawner.grid_size)

        # to search in all the grids around
        for i in range(-1, 2):
            for j in range(-1, 2):
                cell_key = (cell_x + i, cell_y + j)
                if cell_key in enemySpawner.grid:
                    for enemy in enemySpawner.grid[cell_key]:
                        if Collider.check_collision_between(ball, enemy):
                            return enemy
        return False

    def check_collision_between(ball: Ball, enemy: EnemyBall) -> bool:
        distance_squared = (ball.position.posx - enemy.position.posx) ** 2 + (
            ball.position.posy - enemy.position.posy
        ) ** 2
        return distance_squared <= (ball.rad + enemy.rad) ** 2
