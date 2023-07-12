import pygame


class GameSpace:
    """Class managing he game grid on which blocks land"""

    def __init__(self, tet_game) -> None:

        # grid layout
        self.GRID_HEIGHT = 22
        self.GRID_WIDTH = 10
        self.CELL_SIZE = 40

        # screen vairables from main
        self.screen = tet_game.screen
        self.screen_rect = tet_game.screen.get_rect()
        self.WINDOW_HEIGHT = tet_game.WINDOW_HEIGHT
        self.WINDOW_WIDTH = tet_game.WINDOW_WIDTH

        self.grid = [[(0, 0, 0) for col in range(self.GRID_WIDTH)]
                     for row in range(self.GRID_HEIGHT)]

        # set of occupied grid cells
        self.filled = set()

    def draw(self):
        """Class Drawing the game grid to the screen"""

        grid_row = 0

        # determining draw range for columns; grind in the centre of the screen
        # left (start):
        col_draw_range_l = int(self.screen_rect.center[0] -
                               (self.GRID_WIDTH/2)*self.CELL_SIZE)
        # right (limit)
        col_draw_range_r = int(self.screen_rect.center[0] +
                               (self.GRID_WIDTH/2)*self.CELL_SIZE)

        # draw each cell of the grid in the appropriate colour
        for row in range(0, self.WINDOW_HEIGHT, self.CELL_SIZE):
            grid_col = 0
            for col in range(col_draw_range_l, col_draw_range_r, self.CELL_SIZE):
                cell = pygame.Rect(col, row, self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(
                    self.screen, self.grid[grid_row][grid_col], cell)
                grid_col += 1
            grid_col += 1

        # draw grid on top of the cells
        for row in range(0, self.WINDOW_HEIGHT + self.CELL_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, (255, 255, 255),
                             (col_draw_range_l, row), (col_draw_range_r, row), 3)
        for col in range(col_draw_range_l, col_draw_range_r + self.CELL_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, (255, 255, 255),
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
