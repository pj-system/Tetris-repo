from settings import Settings


class TetBot():
    def __init__(self, tet_game: object) -> None:
        settings = Settings()

        #self.playfield = tet_game.playfield

        self.GRID_HEIGHT = settings.GRID_HEIGHT
        self.GRID_WIDTH = settings.GRID_WIDTH

        #self.grid = self.playfield.grid

    def generate_moves(self, grid: list[list], block: list) -> list[list]:
        """Generates all possible moves for a given block"""

        moves = []

        free_space = True
        legal_offset_left = 0

        # Find left most position
        while free_space == True:
            for coor in block:
                if coor[1] - 1 < 0 or block[coor[0]][coor[1] - 1] != (0, 0, 0):
                    free_space = False
                    break
                else:
                    legal_offset_left += 1

        # set block to first legal left most position
        for coor in block:
            coor[1] = coor[1] - legal_offset_left

        return moves

    def calculate_move(self, move: list) -> float:
        """Checks quality of a given move"""
        pass

    def make_move(self):
        """Completes the set of inputs requitred to make the best move in game"""
        pass

    def _evaluate_grid(self, grid: list[list]):
        """Checks for number of gaps created for a given position\n
        A gap is defined as a spece on a grid with which has a block above it but is not it self filled\n
        Checks for columns\n
        Empty pillars are defined as consecutive empty spaces on the grid on top of one another"""
        max_height = 21
        gaps = 0
        empty_pillars = []
        empty_pillar = 0

        for col in range(0, self.GRID_WIDTH):
            # reset top block reached indicator for column and empty pillar height
            top_block_reached = False
            empty_pillar = 0
            # top of filled adjacent col to the edge column - set to bottom inicially
            edge_pillar_check = 21
            for row in range(self.GRID_HEIGHT):
                # if the current cell is empty it is either to be ignored or a gap or a part of an empty pillar
                if grid[row][col] == (0, 0, 0):
                    # if cell is empty and we had a block above, it is a gap
                    if top_block_reached == True:
                        gaps += 1
                    # if we haven't had a block in the column yet we check for pillars:
                    elif col != 0 and col != 9:  # non edge columns
                        if grid[row][col - 1] != (0, 0, 0) or grid[row][col + 1] != (0, 0, 0):
                            empty_pillar += 1
                    else:
                        if col == 0:
                            if grid[row][col + 1] != (0, 0, 0):
                                # if adjacant column has blocks placed higher, we have an empty pillar situation
                                edge_pillar_check = min(edge_pillar_check, row)
                                if row == 21:
                                    empty_pillar = row - edge_pillar_check + 1
                        else:  # column must be == 9
                            if grid[row][col - 1] != (0, 0, 0):
                                # if adjacant column has blocks placed higher, we have an empty pillar situation
                                edge_pillar_check = min(edge_pillar_check, row)
                                if row == 21:
                                    empty_pillar = row - edge_pillar_check + 1
                # if not empty, then it may be the first block in a column (iniciates gap counting), just a space or a bottom of an empty pillar
                else:

                    if top_block_reached == False:
                        edge_pillar_check = min(edge_pillar_check, row)
                        # if an edge column - check empty pillar height, will be negative if no pillar and later ignored
                        if col == 0 or col == 9:
                            empty_pillar = row - edge_pillar_check
                        top_block_reached = True
                        # counter intuative but since top of the grid starts at 0, max hight is the smallest number
                        max_height = min(max_height, row)

            # any pillars over 2 in height are added to the empty pillar list
            if empty_pillar > 2:
                empty_pillars.append(empty_pillar)
                empty_pillar = 0

        return [gaps, empty_pillars, max_height]
