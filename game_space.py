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
        self.grid_colour = (120, 120, 120)

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

    def next_and_saved_grid(self):
        pass

    def check_clear(self) -> int:
        """Checks if Row has been filled up and clears the row.
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
