import pygame
from settings import Settings


class GameSpace:
    """Class managing he game grid on which blocks land"""

    def __init__(self, tet_game) -> None:

        self.scoring = {
            0: 0,
            # single
            1: 40,
            # double
            2: 100,
            # tripple
            3: 300,
            # tetris
            4: 1200
        }

        settings = Settings()
        # grid layout, variables from settings.py
        self.GRID_HEIGHT = settings.GRID_HEIGHT
        self.GRID_WIDTH = settings.GRID_WIDTH
        self.CELL_SIZE = settings.CELL_SIZE
        self.GRID_DRAW_DELTA = settings.GRID_DRAW_DELTA

        self.SIDE_GRID_HIGHT = settings.SIDE_GRID_HIGHT
        self.SIDE_GRID_WIDTH = settings.SIDE_GRID_WIDTH
        self.SIDE_GRID_COL_ORIGIN = settings.SIDE_GRID_COL_ORIGIN

        # screen vairables from main
        self.screen = tet_game.screen
        self.screen_rect = tet_game.screen.get_rect()
        self.WINDOW_HEIGHT = settings.WINDOW_HEIGHT
        self.WINDOW_WIDTH = settings.WINDOW_WIDTH

        # determining draw ranges for main grid (lines); grid to be placed in the centre of the screen
        # column left (start):
        self.col_range_l_main = self.GRID_DRAW_DELTA
        # column right (limit)
        self.col_range_r_main = self.GRID_DRAW_DELTA + self.CELL_SIZE * self.GRID_WIDTH
        # Rop row (top of the screen)
        self.row_range_top_main = 0
        # bottom row (bottom of the screen) **(+ cell size to include bottom line in for loop)
        self.row_range_bot_main = self.WINDOW_HEIGHT + self.CELL_SIZE
        # determining draw range for side gird; grid to be placed in the centre of the screen
        # column left (start):
        self.col_range_l_side = self.SIDE_GRID_COL_ORIGIN
        # column right (limit)
        self.col_range_r_side = self.SIDE_GRID_COL_ORIGIN + \
            self.SIDE_GRID_WIDTH * self.CELL_SIZE
        self.row_range_top_side = [80, 320]
        self.row_range_bot_side = [
            self.SIDE_GRID_HIGHT * self.CELL_SIZE + top for top in self.row_range_top_side]

        # incialise gird storing colours of placed blocks
        self.grid = [[(0, 0, 0) for col in range(self.GRID_WIDTH)]
                     for row in range(self.GRID_HEIGHT)]
        # set grid colour
        self.grid_colour = (120, 120, 120)

    def draw_board(self):
        """Draws the game board (blocks which have been played) to the screen"""

        # draw each cell of the grid in the appropriate colour
        for row in range(0, self.GRID_HEIGHT):

            for col in range(0, self.GRID_WIDTH):
                cell = pygame.Rect(self.col_range_l_main + col * self.CELL_SIZE, row *
                                   self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(
                    self.screen, self.grid[row][col], cell)

    def draw_grid(self):
        """Draws the grid - lines separating the blocks on screen"""

        self._draw_grid_lines(self.row_range_top_main, self.row_range_bot_main,
                              self.col_range_l_main, self.col_range_r_main)

        for grid in range(2):
            self._draw_grid_lines(self.row_range_top_side[grid], self.row_range_bot_side[grid],
                                  self.col_range_l_side, self.col_range_r_side)

    def check_clear(self) -> int:
        """Checks if Row has been filled up and clears the row.\n
        Returns points gained from clearing"""

        # check each row of the grid and if full clear it

        lines_cleared = 0
        points = 0

        for row in range(self.GRID_HEIGHT):
            full = True
            # if any column is empty then no clear
            for col in range(self.GRID_WIDTH):
                if self.grid[row][col] == (0, 0, 0):
                    full = False
                    break
            # if all columns filled - line cleared
            if full == True:
                self.grid.pop(row)
                self.grid.insert(0, [(0, 0, 0)
                                 for col in range(self.GRID_WIDTH)])
                lines_cleared += 1

        points = self.scoring[lines_cleared]
        return points

    def _draw_grid_lines(self, row_range_top: int, row_range_bot: int, col_range_l: int, col_range_r: int):
        """Draws lines of any tetris grid given coordinates of top, bottom, left and right most lines"""
        for row in range(row_range_top, row_range_bot + self.CELL_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.grid_colour,
                             (col_range_l, row), (col_range_r, row), 3)
        for col in range(col_range_l, col_range_r + self.CELL_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.grid_colour,
                             (col, row_range_top), (col, row_range_bot), 3)
