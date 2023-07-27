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

        self.KICK_OPTIONS = [
            # left or right
            [-1, 0], [1, 0],
            # down or up
            [0, 1], [0, -1],
            # down and left or right
            [1, 1], [1, -1],
            # up and left or right
            [-1, 1], [-1, -1]
        ]

        # iniciate settings
        settings = Settings()
        # variables from settings:
        self.GRID_HEIGHT = settings.GRID_HEIGHT
        self.GRID_WIDTH = settings.GRID_WIDTH
        self.CELL_SIZE = settings.CELL_SIZE
        self.GRID_DRAW_DELTA = [0, settings.GRID_DRAW_DELTA]

        # pick a random shape and iniciate corresponding colour
        self.r_selection = random.randint(1, 7)
        self.shape = self.SHAPES[self.r_selection]
        # shape without offset to the middle of the grid:
        self.shape_origin = [coor.copy() for coor in self.shape]
        # find middle of the grid and initialise shape in the middle
        self.set_start()
        # inicialise ghost shape (block shadow) to be in line with the block
        self.ghost_shape = [coor.copy() for coor in self.shape]

        # set colours for block and block shadow:
        self.shape_color = tuple(self.SHAPE_COLOURS[self.r_selection])
        self.ghost_color = (58, 58, 61)

        # set render space to the main screen
        self.screen = tet_game.screen
        self.grid = tet_game.play_field.grid

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
                coor[0] -= max_row - self.GRID_HEIGHT + 1
            self.shape = rotation_shape

        # check if rotated shape exceeds grid limits, if so offset
        edge_check = False
        # left side
        if min_col < 0:
            offset = 0 - min_col
            edge_check = True
        # right side
        if max_col >= self.GRID_WIDTH:
            offset = self.GRID_WIDTH - max_col - 1
            edge_check = True
        # if beyond one of the edges -> offset
        if edge_check:
            for coor in rotation_shape:
                coor[1] += offset

        # check colisions with other blocks and attempt to relocate 1 space in any direction
        if not self._check_placed_collision(rotation_shape):
            for kick in self.KICK_OPTIONS:
                test_rotation_shape = list(rotation_shape)
                for coor in test_rotation_shape:
                    coor[0] += kick[0]
                    coor[1] += kick[1]
                if self._check_placed_collision(test_rotation_shape):
                    self.shape = test_rotation_shape
                    return

        self.shape = rotation_shape
        return

    def draw(self):
        """class responisble for drawing block currently in play onto the screen"""

        self._update_ghost()

        for i in range(4):
            coordinate = self.ghost_shape[i]
            self._draw_shape(
                coordinate, self.GRID_DRAW_DELTA, self.ghost_color)

        for i in range(4):
            coordinate = self.shape[i]
            self._draw_shape(coordinate, self.GRID_DRAW_DELTA,
                             self.shape_color)

    def draw_tetromino(self, origin: list):
        """Draws the block shape in any postion relative to the origin.\n
        Origin takers Row then column (Y -> X)"""
        for i in range(4):
            coordinate = self.shape_origin[i]
            self._draw_shape(coordinate, origin,
                             self.shape_color)

    def update(self) -> bool:
        """If possible, shifts block down by one on the grid.\n
            Returns True if block moved"""

        # check if block doesn't colide with existing blocks or hit the bottom
        if not self._check_free_space(self.shape):
            return None

        # if not at the bottom or on top of another block: move each part of the piece down 1 cell
        for i in range(len(self.shape)):
            self.shape[i][0] += 1
        return True

    def move(self, direction: int):
        """Moves the block when arrow key is pressed. Needs grid array to check collisions"""
        for i in range(len(self.shape)):

            # row coorindate to check
            next_coor = self.shape[i][1] + direction
            # row coorinate of the block on the grid
            block_coor = self.shape[i]

            # do nothing if move is not allowed
            if next_coor == self.GRID_WIDTH or next_coor < 0:
                return

            if self.grid[block_coor[0]][next_coor] != (0, 0, 0):
                return

        # shift all blocks in the directon of key press
        for i in range(len(self.shape)):
            self.shape[i][1] += direction

    def hard_drop_block(self) -> int:
        """Drops the block to the lowest point possible on the grid.\n
        Returns no. of lines dropped for scoring"""

        lines_dropped = 0

        # keep dropping the block by one until it either hits the bottom or another block
        while self._check_free_space(self.shape):
            for i in range(len(self.shape)):
                self.shape[i][0] += 1
            lines_dropped += 1

        return lines_dropped

    def set_start(self):

        self.shape = [coor.copy() for coor in self.shape_origin]
        for i in range(4):
            self.shape[i][1] += int((self.GRID_WIDTH/2)) - 2

    def _check_free_space(self, shape: list) -> bool:
        """Checks whether it is possible to move the block down by one increment"""

        for i in range(4):
            # column and row to be checked
            col_check = shape[i][1]
            row_check = shape[i][0] + 1

            # check bottom
            if row_check == self.GRID_HEIGHT:
                return False
            # check collsion
            if self.grid[row_check][col_check] != (0, 0, 0):
                return False

        return True

    def _check_placed_collision(self, shape: list) -> bool:
        """Checks if shape resulting from rotation is beyond the grid space or collides with placed blocks.\n
        Returns True if location is valid"""
        for coor in shape:
            row, col = coor[0], coor[1]
            # Grid check
            if row >= self.GRID_HEIGHT or col < 0 or col >= self.GRID_WIDTH:
                return False
            # block colision check
            if self.grid[row][col] != (0, 0, 0):
                return False
        return True

    def _draw_shape(self, coordinate: list, delta: list, colour: tuple):
        """Draws game blocks to the game screen.\n
        coordinate: list in form: [row][col].\n
        delta: offset relative to the screen size"""

        block_section = pygame.Rect(delta[1] + coordinate[1] * self.CELL_SIZE, delta[0] + coordinate[0] * self.CELL_SIZE,
                                    self.CELL_SIZE, self.CELL_SIZE)
        pygame.draw.rect(self.screen, colour, block_section)

    def _update_ghost(self):
        """Updates the position of the ghost (shadow indicating block position if dropped)"""

        self.ghost_shape = [coor.copy() for coor in self.shape]
        while self._check_free_space(self.ghost_shape):
            for i in range(len(self.ghost_shape)):
                self.ghost_shape[i][0] += 1
