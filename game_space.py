import pygame


class GameSpace:
    """Class managing he game grid on which blocks land"""

    def __init__(self, tet_game) -> None:

        # grid layout
        self.GRID_HEIGHT = 22
        self.GRID_WIDTH = 10
        self.CELL_SIZE = 40

        self.screen = tet_game.screen
        self.WINDOW_HEIGHT = tet_game.WINDOW_HEIGHT
        self.WINDOW_WIDTH = tet_game.WINDOW_WIDTH

        # set of occupied grid cells
        self.filled = set()

    def draw(self):
        for row in range(0, self.WINDOW_HEIGHT, self.CELL_SIZE):

            # note to self - I don't like how this is atm, FIX LATER!!!
            for col in range(int(self.WINDOW_WIDTH/4), int(self.WINDOW_WIDTH/4)*3, self.CELL_SIZE):
                cell = pygame.Rect(col, row, self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(self.screen, (3, 60, 89), cell, 2)

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
