import random


class Block:
    """Class managing the game shapes"""

    shapes = {
        1: [(1, -1), (1, 0), (0, -1), (0, 0)],
        2: [(0, -2), (0, -1), (0, 0), (0, 1)],
        3: [(1, -2), (0, -2), (0, -1), (0, 0)],
        4: [(1, 0), (0, -2), (0, -1), (0, 0)],
        5: [(1, -1), (1, 0), (0, -2), (0, -1)],
        6: [(1, -2), (1, -1), (0, -1), (0, 0)],
        7: [(1, -1), (0, -2), (0, -1), (0, 0)]
    }

    def __init__(self) -> None:
        self.shape = random.randint(1, 7)

    def rotate(self):
        pass
