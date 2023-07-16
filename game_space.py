import pygame
from settings import Settings


class GameSpace:
    """Class managing he game grid on which blocks land"""

    def __init__(self, tet_game) -> None:

        settings = Settings()
        # grid layout
        self.GRID_HEIGHT = settings.GRID_HEIGHT
        self.GRID_WIDTH = settings.GRID_WIDTH
        self.CELL_SIZE = settings.CELL_SIZE
        self.GRID_DRAW_DELTA = settings.GRID_DRAW_DELTA

        # determining draw range for columns; grid to be placed in the centre of the screen
        # left (start):
        self.col_draw_range_l = self.GRID_DRAW_DELTA
        # right (limit)
        self.col_draw_range_r = self.GRID_DRAW_DELTA + self.CELL_SIZE * self.GRID_WIDTH

        # screen vairables from main
        self.screen = tet_game.screen
        self.screen_rect = tet_game.screen.get_rect()
        self.WINDOW_HEIGHT = settings.WINDOW_HEIGHT
        self.WINDOW_WIDTH = settings.WINDOW_WIDTH

        self.grid = [[(0, 0, 0) for col in range(self.GRID_WIDTH)]
                     for row in range(self.GRID_HEIGHT)]
        self.grid_colour = (200, 200, 200)

        # set of occupied grid cells
        self.filled = set()

    def draw_board(self):
        """Draws the game board (blocks which have been played) to the screen"""

        # draw each cell of the grid in the appropriate colour
        for row in range(0, self.GRID_HEIGHT):

            for col in range(0, self.GRID_WIDTH):
                cell = pygame.Rect(self.col_draw_range_l + col * self.CELL_SIZE, row *
                                   self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(
                    self.screen, self.grid[row][col], cell)

    def draw_grid(self):
        """Draws the grid - lines separating the blocks on screen"""

        for row in range(0, self.WINDOW_HEIGHT + self.CELL_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.grid_colour,
                             (self.col_draw_range_l, row), (self.col_draw_range_r, row), 3)
        for col in range(self.col_draw_range_l, self.col_draw_range_r + self.CELL_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.grid_colour,
                             (col, 0), (col, self.WINDOW_HEIGHT), 3)

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
