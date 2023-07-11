import random


class Block:
    """Class managing the game shapes"""

    SHAPES = {
        1: [(1, -1), (1, 0), (0, -1), (0, 0)],
        2: [(0, -2), (0, -1), (0, 0), (0, 1)],
        3: [(1, -2), (0, -2), (0, -1), (0, 0)],
        4: [(1, 0), (0, -2), (0, -1), (0, 0)],
        5: [(1, -1), (1, 0), (0, -2), (0, -1)],
        6: [(1, -2), (1, -1), (0, -1), (0, 0)],
        7: [(1, -1), (0, -2), (0, -1), (0, 0)]
    }

    SHAPE_COLOURS = {
        1: (232, 225, 9),
        2: (9, 225, 232),
        3: (17, 32, 242),
        4: (232, 225, 9),
        5: (232, 225, 9),
        6: (232, 225, 9),
        7: (232, 225, 9),

    }

    def __init__(self, tet_game) -> None:

        # pick a random shape and iniciate corresponding colour
        r_selection = random.randint(1, 7)
        self.shape = self.SHAPES[r_selection]
        self.shape_color = self.SHAPE_COLOURS[r_selection]

        self.location = self.shape.copy()
        self.screen = tet_game.screen

    def rotate(self):
        pass

    def draw():
        pass

    def update():
        pass
