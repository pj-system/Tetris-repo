class Settings():
    """class holding game settings"""

    def __init__(self) -> None:

        # grid size
        self.GRID_HEIGHT = 22
        self.GRID_WIDTH = 10
        self.CELL_SIZE = 40

        # grid for saved and next shapes
        self.SIDE_GRID_HIGHT = 3
        self.SIDE_GRID_WIDTH = 5

        # window dimentions and attributes
        self.WINDOW_HEIGHT = 880
        self.WINDOW_WIDTH = 880

        self.WINDOW_CENTER = int(self.WINDOW_WIDTH/2)

        # calulate left most position of the grid for a given screen size
        self.GRID_DRAW_DELTA = int(self.WINDOW_CENTER -
                                   (self.CELL_SIZE * (self.GRID_WIDTH/2)))

        # calculate location of the side grids
        self.SIDE_GRID_COL_ORIGIN = int(self.WINDOW_WIDTH - self.GRID_DRAW_DELTA + (
            self.GRID_DRAW_DELTA - self.SIDE_GRID_WIDTH * self.CELL_SIZE)/2)

        # speed of blocks falling down (once every x ms)
        self.drop_rate = 800
        self.accelerate = 50


# x = Settings()
# print(x.WINDOW_CENTER)
# print(x.GRID_DRAW_IND)
