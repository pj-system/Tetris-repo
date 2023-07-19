import sys
import pygame

from game_blocks import Block
from game_space import GameSpace
from settings import Settings


class Tetris:
    """Class managing game assets and behaviour"""

    def __init__(self) -> None:

        pygame.init
        settings = Settings()
        # Game window size
        self.WINDOW_HEIGHT = settings.WINDOW_HEIGHT
        self.WINDOW_WIDTH = settings.WINDOW_WIDTH

        # intitalise game window
        self.screen = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("TETRIS")

        self.play_field = GameSpace(self)
        self.block = Block(self)

        # set user event to periodically lower the block and timer for block drop event
        self.drop_rate = settings.drop_rate
        self.accelerate_rate = settings.accelerate
        self.drop_block = pygame.USEREVENT + 0
        pygame.time.set_timer(self.drop_block, self.drop_rate)

        self.clock = pygame.time.Clock()

    def run_game(self):
        """Main loop of the game"""
        while True:
            # Event Check
            self.check_events()

            # Game Logic

            # tbc

            # window background and UI
            self.screen.fill((0, 0, 0))

            # Graphics render
            self.play_field.draw_board()
            self.block.draw()
            self.play_field.draw_grid()

            # Refresh display at 60fps
            pygame.display.flip()

            self.clock.tick(60)

    def check_events(self):
        """Checks for player input - mouse and keyboard"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Keyboard input
            # key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_RIGHT:
                    self.block.move(1, self.play_field.grid)
                if event.key == pygame.K_LEFT:
                    self.block.move(-1, self.play_field.grid)
                if event.key == pygame.K_DOWN:
                    self._accelerate_block()
                if event.key == pygame.K_UP:
                    self.block.rotate()
            # key release
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self._decelerate_block()

            # block drop on timer
            if event.type == self.drop_block:
                if not self.block.update(self.play_field.grid):
                    self._add_to_grid()
                    self.play_field.check_clear()
                    self.block = Block(self)

    def _add_to_grid(self):
        """Helper method updating the grid once the block lands"""
        for coor in self.block.shape:
            grid_row, grid_col = coor[0], coor[1]
            self.play_field.grid[grid_row][grid_col] = self.block.shape_color

    def _accelerate_block(self):
        pygame.time.set_timer(self.drop_block, self.accelerate_rate)

    def _decelerate_block(self):
        pygame.time.set_timer(self.drop_block, self.drop_rate)


game = Tetris()
game.run_game()
