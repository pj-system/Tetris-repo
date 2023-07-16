class Settings():
    """class holding game settings"""

    def __init__(self) -> None:

        # grid size
        self.GRID_HEIGHT = 22
        self.GRID_WIDTH = 10
        self.CELL_SIZE = 40

        # window dimentions and attributes
        self.WINDOW_HEIGHT = 880
        self.WINDOW_WIDTH = 800

        self.WINDOW_CENTER = int(self.WINDOW_WIDTH/2)

        # calulate left most position of the grid for a given screen size
        self.GRID_DRAW_DELTA = int(self.WINDOW_CENTER -
                                   (self.CELL_SIZE * (self.GRID_WIDTH/2)))

        # speed of blocks falling down (once every x ms)
        self.drop_rate = 500


# x = Settings()
# print(x.WINDOW_CENTER)
# print(x.GRID_DRAW_IND)
