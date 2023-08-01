from settings import Settings


class TetBot():
    def __init__(self, tet_game: object) -> None:
        settings = Settings()

        self.playfield = tet_game.playfield

        self.GRID_HEIGHT = settings.GRID_HEIGHT
        self.GRID_WIDTH = settings.GRID_WIDTH

        self.grid = self.playfield.grid

    def generate_moves(self):
        """Generates all possible moves for a given block"""
        pass

    def calculate_move(self, move: list):
        """Checks quality of a given move"""
        pass

    def make_move(self):
        """Completes the set of inputs requitred to make the best move in game"""
        pass

    def _evaluate_grid(self, grid: list):
        """Checks for number of gaps created for a given position\n
        A gap is defined as a spece on a grid with which has a block above it but is not it self filled\n
        Checks for columns\n
        Columns are defined as consecutive empty spaces on the grid on top of one another"""
        max_height = 0
        gaps = 0
        columns = []
        columns_over_4 = 0

        for col in range(0, self.GRID_WIDTH + 1):
            for row in range(self.GRID_HEIGHT + 1):
                pass
