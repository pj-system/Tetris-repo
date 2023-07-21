import random
from settings import Settings
import pygame


class Block:
    """Class managing the game shapes (blocks)"""

    def __init__(self, tet_game) -> None:
        # dict of shapes (top left corner idicated / grid location)
        self.SHAPES = {
            # I
            1: [[1, 0], [1, 1], [1, 2], [1, 3]],
            # J
            2: [[0, 0], [1, 0], [1, 1], [1, 2]],
            # L
            3: [[0, 2], [1, 0], [1, 1], [1, 2]],
            # O
            4: [[0, 1], [0, 2], [1, 1], [1, 2]],
            # S
            5: [[0, 1], [0, 2], [1, 1], [1, 0]],
            # Z
            6: [[0, 0], [0, 1], [1, 1], [1, 2]],
            # T
            7: [[0, 1], [1, 0], [1, 1], [1, 2]]
        }

        self.SHAPE_COLOURS = {
            1: (66, 218, 245),
            2: (23, 33, 230),
            3: (230, 144, 23),
            4: (245, 221, 10),
            5: (20, 219, 13),
            6: (209, 29, 29),
            7: (133, 12, 199),

        }

        # iniciate settings
        settings = Settings()

        # pick a random shape and iniciate corresponding colour
        self.r_selection = random.randint(1, 7)
        self.shape = self.SHAPES[self.r_selection]
        self.shape_color = tuple(self.SHAPE_COLOURS[self.r_selection])

        # set render space to the main screen
        self.screen = tet_game.screen

        self.GRID_HEIGHT = settings.GRID_HEIGHT
        self.GRID_WIDTH = settings.GRID_WIDTH
        self.CELL_SIZE = settings.CELL_SIZE
        self.GRID_DRAW_DELTA = settings.GRID_DRAW_DELTA

        self.loc_row = 0
        self.loc_col = int((self.GRID_WIDTH/2)) - 2

        for i in range(len(self.shape)):
            self.shape[i][1] += self.loc_col

    def rotate(self):
        """Rotates the piece in play"""

        # Do nothing if shape is an O
        if self.r_selection == 4:
            return

        # SHAPES dict is constructed so pivot block is always in positin 2
        pivot = self.shape[2]
        rotation_shape = [0, 0, 0, 0]

        for i in range(4):
            coor = self.shape[i]
            row, col = pivot[0] - coor[0], pivot[1] - coor[1]
            rotation_shape[i] = [col * -1 + pivot[0], row * 1 + pivot[1]]

        # maxrow - lowest position of the block, min/max_col - left and right most postion
        max_row = max((x[0]) for x in rotation_shape)
        min_col = min((x[1]) for x in rotation_shape)
        max_col = max((x[1]) for x in rotation_shape)

        # check if post rotation shape dips below the lowest points of the grid, elvate by 1 if so
        if max_row >= self.GRID_HEIGHT:
            for coor in rotation_shape:
                if self.r_selection == 1:
                    coor[0] -= max_row - self.GRID_HEIGHT + 1
                else:
                    coor[0] -= 1
            self.shape = rotation_shape

        # check if rotated shape exceeds grid limits, if so offset
        edge_check = False
        # left side
        if min_col < 0:
            offset = 0 - min_col
            edge_check = True
        if max_col >= self.GRID_WIDTH:
            offset = self.GRID_WIDTH - max_col - 1
            edge_check = True
        # right side
        if edge_check:
            for coor in rotation_shape:
                print(offset)
                coor[1] += offset
            self.shape = rotation_shape
        else:
            self.shape = rotation_shape

    def draw(self):
        """class responisble for drawing block currently in play onto the screen"""
        for coordinate in self.shape:
            block_section = pygame.Rect(self.GRID_DRAW_DELTA + coordinate[1] * self.CELL_SIZE, coordinate[0] * self.CELL_SIZE,
                                        self.CELL_SIZE, self.CELL_SIZE)
            pygame.draw.rect(self.screen, self.shape_color, block_section)

    def update(self, grid):
        """shift block down by one on the grid
            Returns True if blocked moved"""

        # check if block doesn't colide with existing blocks or hit the bottom
        if not self._check_free_space(grid):
            return None

        # if not at the bottom or on top of another block: move each part of the piece down 1 cell
        for i in range(len(self.shape)):
            self.shape[i][0] += 1
        return True

    def move(self, direction: int, grid: list[list]):
        """ moves the block when arrow key is pressed. Needs grid array to check collisions"""
        for i in range(len(self.shape)):

            # row coorindate to check
            next_coor = self.shape[i][1] + direction
            # row coorinate of the block on the grid
            block_coor = self.shape[i]

            if next_coor == self.GRID_WIDTH or next_coor < 0:
                return

            if next_coor < self.GRID_WIDTH - 1:
                if grid[block_coor[0]][next_coor] != (0, 0, 0):
                    return

        # shift all blocks in the directon of key press
        for i in range(len(self.shape)):
            self.shape[i][1] += direction

    def drop_block(self, grid):
        """Drops the block the lowest point possible on the grid"""

        # keep dropping the block by one until it either hits the bottom or another block
        while self._check_free_space(grid):
            for i in range(len(self.shape)):
                self.shape[i][0] += 1

    def _check_free_space(self, grid) -> bool:
        """Checks whether it is possible to move the block down by one increment"""

        for i in range(4):
            # column and row to be checked
            col_check = self.shape[i][1]
            row_check = self.shape[i][0] + 1

            # check bottom
            if row_check == self.GRID_HEIGHT:
                return False
            # check collsion
            if grid[row_check][col_check] != (0, 0, 0):
                return False

        return True
