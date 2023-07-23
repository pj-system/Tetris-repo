import sys
import pygame

from game_blocks import Block
from game_space import GameSpace
from settings import Settings


class Tetris:
    """Class managing game assets and behaviour"""

    def __init__(self) -> None:

        pygame.init()
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
        self.next_block = Block(self)

        # set user event to periodically lower the block and timer for block drop event
        self.drop_rate = settings.drop_rate
        self.accelerate_rate = settings.accelerate
        self.soft_drop_block = pygame.USEREVENT + 0
        pygame.time.set_timer(self.soft_drop_block, self.drop_rate)

        self.clock = pygame.time.Clock()
        self.text_font = pygame.font.SysFont("arial", 25, True)

        self.score = 0

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
            # COME BACK TO THIS!!!!
            self.next_block.draw_tetromino([80, 700])
            self.play_field.draw_grid()
            self.draw_score()

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
                    self.block.move(1)
                if event.key == pygame.K_LEFT:
                    self.block.move(-1)
                if event.key == pygame.K_DOWN:
                    self._accelerate_block()
                if event.key == pygame.K_UP:
                    self.block.rotate()
                # Restart
                if event.key == pygame.K_r:
                    self.reset()
                if event.key == pygame.K_SPACE:
                    self._drop_and_add_score()
                    self._new_block()
            # key release
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self._decelerate_block()

            # block drop on timer
            if event.type == self.soft_drop_block:
                if not self.block.update():
                    self._add_to_grid()
                    self.score += self.play_field.check_clear()
                    self._new_block()

    def draw_score(self):
        heading = self.text_font.render("SCORE:", True, (255, 255, 255))
        self.screen.blit(heading, (25, 25))

        score_text = self.text_font.render(
            f'{self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (25, 60))

    def reset(self):
        self.play_field = GameSpace(self)
        self.block = Block(self)
        self.score = 0

    def _add_to_grid(self):
        """Helper method updating the grid once the block lands"""
        for coor in self.block.shape:
            grid_row, grid_col = coor[0], coor[1]
            self.play_field.grid[grid_row][grid_col] = self.block.shape_color

    def _accelerate_block(self):
        """increases soft drop rate of the block"""
        pygame.time.set_timer(self.soft_drop_block, self.accelerate_rate)

    def _decelerate_block(self):
        """decreases soft drop rate to baseline"""
        pygame.time.set_timer(self.soft_drop_block, self.drop_rate)

    def _drop_and_add_score(self):
        lines_dropped = self.block.hard_drop_block()
        self._add_to_grid()
        clear_score = self.play_field.check_clear()
        if clear_score > 0:
            self.score += clear_score + lines_dropped + 1

    def _new_block(self):
        self.block = self.next_block
        self.next_block = Block(self)


game = Tetris()
game.run_game()
