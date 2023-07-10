import pygame


class GameSpace:
    """Class managing he game grid on which blocks land"""

    def __init__(self, tetris) -> None:
        self.GRID_HEIGHT = 22
        self.GRID_WIDTH = 10
        self.screen = tetris.screen

        # set of occupied grid cells
        self.filled = set()

    def draw(self):
        pass

    def check_clear(self):
        """Checks if Tetris has been achieved"""

        rows_in_play = dict()

        # add number of filled cells in each used row: Key = row (int), Value = no. of filled cells
        for item in self.filled:
            rows_in_play[item[0]] = rows_in_play.get(item[0], 0) + 1

        # if filled cells > 10 then tetris achieved
        for row in rows_in_play:
            if row.value == 10:
                # remove teris row cells from occupied cells set
                for cell in self.filled():
                    if cell[0] == row:
                        self.filled.remove(cell)
